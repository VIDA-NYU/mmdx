import os
import lancedb
import pandas as pd
import pyarrow as pa
from .model import BaseEmbeddingModel
from .db import LabelsDB
from .settings import DB_BATCH_SIZE, DB_BATCH_LOAD, DEFAULT_TABLE_NAME, DATA_SAMPLE_SIZE
import duckdb
from typing import Iterator
import numpy as np
import duckdb
import random
import tqdm


duckdb.sql(
    """
    INSTALL sqlite;
    LOAD sqlite;
    """
)


def find_files_in_path(path, file_extensions=(".png", ".jpg", "jpeg")) -> Iterator[str]:
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith(file_extensions):
                relative_dir = dirpath.replace(path, "")
                file_path = os.path.join(relative_dir, filename)
                yield file_path


def load_batches(
    db: lancedb.DBConnection, table_name: str, data_path: str, model: BaseEmbeddingModel
) -> lancedb.table.Table:
    image_files = list(find_files_in_path(data_path))
    print(f"Found {len(image_files)} images in {data_path}")

    if DATA_SAMPLE_SIZE is not None:
        print(f"Sampling {DATA_SAMPLE_SIZE} out of {len(image_files)} images...")
        image_files = random.sample(image_files, DATA_SAMPLE_SIZE)

    batch_size = DB_BATCH_SIZE

    def make_batches() -> pa.RecordBatch:
        for i in tqdm.tqdm(range(0, len(image_files), batch_size)):
            image_paths = image_files[i : i + batch_size]
            embeddings = [
                model.embed_image_path(os.path.join(data_path, path))
                for path in image_paths
            ]
            image_paths_array = pa.array(image_paths)
            embeddings_array = pa.array(
                embeddings, pa.list_(pa.float32(), model.dimensions())
            )
            yield pa.RecordBatch.from_arrays(
                [
                    image_paths_array,
                    embeddings_array,
                ],
                [
                    "image_path",
                    "vector",
                ],
            )

    db_schema = pa.schema(
        [
            pa.field("image_path", pa.utf8()),
            pa.field("vector", pa.list_(pa.float32(), model.dimensions())),
        ]
    )
    tbl = db.create_table(
        table_name,
        make_batches(),
        schema=db_schema,
    )
    # tbl.add(make_batches(data_path, image_files, model))
    return tbl


def make_df(data_path: str, model: BaseEmbeddingModel):
    image_files = list(find_files_in_path(data_path))
    print(f"Found {len(image_files)} images in {data_path}")

    if DATA_SAMPLE_SIZE is not None:
        print(f"Sampling {DATA_SAMPLE_SIZE} out of {len(image_files)} images...")
        image_files = random.sample(image_files, DATA_SAMPLE_SIZE)

    image_paths = []
    vectors = []
    for image_path in tqdm.tqdm(image_files):
        embedding = model.embed_image_path(
            image_path=os.path.join(data_path, image_path)
        )
        vectors.append(embedding)
        image_paths.append(image_path)

    df = pd.DataFrame(
        {
            "image_path": image_paths,
            "vector": vectors,
        }
    )
    return df


class VectorDB:
    def __init__(
        self,
        db_path: str,
        db: lancedb.DBConnection,
        table: lancedb.table.Table,
        model: BaseEmbeddingModel,
        data_path: str,
    ) -> None:
        self.db = db
        self.model = model
        self.tbl = table
        self.data_path = data_path
        self.labelsdb_path = os.path.join(db_path, "labels.db")
        self.labelsdb = LabelsDB(self.labelsdb_path)

    @staticmethod
    def from_data_path(
        data_path: str,
        db_path: str,
        model: BaseEmbeddingModel,
        delete_existing=True,
        batch_load: bool = DB_BATCH_LOAD,
    ):
        db = lancedb.connect(db_path)

        table_name = DEFAULT_TABLE_NAME
        if delete_existing and table_name in db.table_names():
            print(f"Dropping existing database {table_name}...")
            db.drop_table(table_name)
            print("done.")

        if table_name in db.table_names():
            print(f'Opening existing table "{table_name}"...')
            tbl = db.open_table(table_name)
            return VectorDB(db_path, db, tbl, model, data_path)
        else:
            print(f'Creating table "{table_name}"...')
            if batch_load:
                tbl = load_batches(db, table_name, data_path, model)
            else:
                tbl = db.create_table(table_name, data=make_df(data_path, model))
            return VectorDB(db_path, db, tbl, model, data_path)

    def count_rows(self) -> int:
        return len(self.tbl)

    def get(self, image_path: str) -> pd.DataFrame:
        lance_tbl = self.tbl.to_lance()
        return duckdb.sql(
            f"SELECT * FROM lance_tbl WHERE image_path='{image_path}';"
        ).to_df()

    def add_label(self, image_path: str, label: str):
        self.labelsdb.add(image_path=image_path, label=label)

    def remove_label(self, image_path: str, label: str):
        self.labelsdb.remove(image_path=image_path, label=label)

    def get_labels(self, image_path: str = None) -> list[str]:
        return self.labelsdb.get(image_path=image_path)

    def random_search(self, limit: int) -> pd.DataFrame:
        lance_tbl = self.tbl.to_lance()
        df_hits = duckdb.sql(
            f"""
            SELECT lance_tbl.*, grouped_labels.labels FROM lance_tbl
            LEFT OUTER JOIN (
                SELECT image_path, list(label) AS labels FROM sqlite_scan('{self.labelsdb_path}', 'labels') GROUP BY image_path
            ) AS grouped_labels
            ON (lance_tbl.image_path = grouped_labels.image_path)
            USING SAMPLE {limit} ROWS;
        """
        ).to_df()
        df_hits["labels"] = df_hits["labels"].fillna("").apply(list)
        df_hits.drop(columns=["vector"], inplace=True)
        return df_hits

    def search_by_image_path(self, image_path: str, limit: int) -> pd.DataFrame:
        full_image_path = os.path.join(self.data_path, image_path)
        image_embedding = self.model.embed_image_path(full_image_path)
        df_hits = self.__vector_embedding_search(
            image_embedding, limit, exclude_image_path=image_path
        )
        return df_hits

    def search_by_text(self, query_string: str, limit: int) -> pd.DataFrame:
        query_str_embedding = self.model.embed_text(query=query_string)
        df_hits = self.__vector_embedding_search(query_str_embedding, limit)
        return df_hits

    def __vector_embedding_search(
        self, embedding: np.ndarray, limit: int, exclude_image_path=str
    ) -> pd.DataFrame:
        df_hits = self.tbl.search(embedding).limit(limit + 1).to_df()
        if exclude_image_path is not None:
            df_hits = df_hits[df_hits["image_path"] != exclude_image_path][0:limit]
        df_hits.drop(columns=["vector"], inplace=True)
        df_hits = self.__join_labels(left_table=df_hits)
        return df_hits

    def __join_labels(self, left_table: pd.DataFrame) -> pd.DataFrame:
        df_join = duckdb.sql(
            f"""
            SELECT left_table.*, grouped_labels.labels FROM left_table
            LEFT OUTER JOIN (
                SELECT image_path, list(label) AS labels FROM sqlite_scan('{self.labelsdb_path}', 'labels') GROUP BY image_path
            ) AS grouped_labels
            ON (left_table.image_path = grouped_labels.image_path)
            ORDER BY left_table._distance ASC;
        """
        ).to_df()
        df_join["labels"] = df_join["labels"].fillna("").apply(list)
        return df_join
