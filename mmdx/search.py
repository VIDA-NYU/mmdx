import os
import lancedb
import pandas as pd
import pyarrow as pa
from .model import BaseEmbeddingModel
import duckdb
from typing import Iterator


DB_BATCH_SIZE = 32
DB_BATCH_LOAD = False
DEFAULT_TABLE_NAME = "images"


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
    batch_size = DB_BATCH_SIZE

    def make_batches() -> pa.RecordBatch:
        for i in range(0, len(image_files), batch_size):
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
    image_paths = []
    vectors = []
    for image_path in find_files_in_path(data_path):
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
        db: lancedb.DBConnection,
        table: lancedb.table.Table,
        model: BaseEmbeddingModel,
        data_path: str,
    ) -> None:
        self.db = db
        self.model = model
        self.tbl = table
        self.data_path = data_path

        self.df_labels = pd.DataFrame(
            {
                "image_path": pd.Series(dtype="str"),
                "label": pd.Series(dtype="str"),
            }
        )

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
            return VectorDB(db, tbl, model, data_path)
        else:
            print(f'Creating table "{table_name}"...')
            if batch_load:
                tbl = load_batches(db, table_name, data_path, model)
            else:
                tbl = db.create_table(table_name, data=make_df(data_path, model))
            return VectorDB(db, tbl, model, data_path)

    def count_rows(self) -> int:
        return len(self.tbl)

    def get(self, image_path: str) -> pd.DataFrame:
        lance_tbl = self.tbl.to_lance()
        return duckdb.sql(
            f"SELECT * FROM lance_tbl WHERE image_path='{image_path}';"
        ).to_df()

    def add_label(self, image_path: str, label: str):
        df_new_data = pd.DataFrame([{"image_path": image_path, "label": label}])
        self.df_labels = pd.concat([self.df_labels, df_new_data], ignore_index=True)

    def remove_label(self, image_path: str, label: str):
        df_new_data = pd.DataFrame([{"image_path": image_path, "label": label}])
        self.df_labels = pd.concat([self.df_labels, df_new_data], ignore_index=True)
        mask = (self.df_labels["image_path"] == image_path) & (
            self.df_labels["label"] == label
        )
        self.df_labels.drop(mask.index, inplace=True)

    def get_labels(self, image_path: str = None) -> list[str]:
        if image_path is None:
            return list(self.df_labels["label"].unique())
        else:
            df_labels = self.df_labels[self.df_labels["image_path"] == image_path]
            return df_labels["label"].to_list()

    def random_search(self, limit: int) -> pd.DataFrame:
        lance_tbl = self.tbl.to_lance()
        labels_tbl = (
            self.df_labels.groupby(by="image_path")["label"]
            .apply(list)
            .reset_index(name="labels")
        )
        print(f"GroupBy Labels: {len(labels_tbl)} {list(labels_tbl.columns)}")
        print(labels_tbl)
        # return duckdb.sql(f"SELECT * FROM lance_tbl USING SAMPLE {limit};").to_df()
        df_hits = duckdb.sql(
            f"""
            SELECT lance_tbl.*, labels FROM lance_tbl
            LEFT OUTER JOIN labels_tbl ON (lance_tbl.image_path = labels_tbl.image_path)
            USING SAMPLE {limit} ROWS;
        """
        ).to_df()
        df_hits["labels"] = df_hits["labels"].fillna("").apply(list)
        df_hits.drop(columns=["vector"], inplace=True)
        return df_hits

    def search_by_image_path(self, image_path: str, limit: int) -> pd.DataFrame:
        full_image_path = os.path.join(self.data_path, image_path)
        df_hits = (
            self.tbl.search(self.model.embed_image_path(full_image_path))
            .limit(limit + 1)
            .to_df()
        )
        df_hits = df_hits[df_hits["image_path"] != image_path][0:limit]

        df_hits = self.__load_labels(df_hits)
        df_hits.drop(columns=["vector"], inplace=True)
        return df_hits

    def search_by_text(self, query_string: str, limit: int) -> pd.DataFrame:
        df_hits = (
            self.tbl.search(self.model.embed_text(query=query_string))
            .limit(limit)
            .to_df()
        )
        df_hits = self.__load_labels(df_hits)
        df_hits.drop(columns=["vector"], inplace=True)
        return df_hits

    def __load_labels(self, df_hits: pd.DataFrame) -> pd.DataFrame:
        labels_tbl = (
            self.df_labels.groupby(by="image_path")["label"]
            .apply(list)
            .reset_index(name="labels")
        )
        df_hits = pd.merge(how="left", left=df_hits, right=labels_tbl, on="image_path")
        df_hits["labels"] = df_hits["labels"].fillna("").apply(list)
        return df_hits
