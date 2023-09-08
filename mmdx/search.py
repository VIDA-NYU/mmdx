import os
import lancedb
import pandas as pd
from PIL import Image
import pyarrow as pa
from .model import BaseEmbeddingModel
import duckdb
import pyarrow as pa
from typing import Iterator
from lance.vector import vec_to_table
import numpy as np
import pyarrow


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


def make_batches(
    data_path: str,
    all_files: list[str],
    model: BaseEmbeddingModel,
    batch_size=DB_BATCH_SIZE,
) -> pa.RecordBatch:
    for i in range(0, len(all_files), batch_size):
        image_paths = all_files[i : i + batch_size]
        embeddings = [
            model.embed_image_path(os.path.join(data_path, path))
            for path in image_paths
        ]
        image_paths_array = pa.array(image_paths)
        embeddings_array = pa.array(
            embeddings, pa.list_(pa.float32(), model.dimensions())
        )
        yield pa.RecordBatch.from_arrays(
            [image_paths_array, embeddings_array],
            ["image_path", "vector"],
        )


def load_batches(
    db: lancedb.DBConnection, table_name: str, data_path: str, model: BaseEmbeddingModel
) -> lancedb.table.Table:
    image_files = list(find_files_in_path(data_path))
    db_schema = pa.schema(
        [
            pa.field("image_path", pa.utf8()),
            pa.field("vector", pa.list_(pa.float32(), model.dimensions())),
        ]
    )
    tbl = db.create_table(
        table_name,
        make_batches(data_path, image_files, model),
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
            print(f"Droping existing database {table_name}...")
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

    def count_rows(self) -> pd.DataFrame:
        lance_tbl = self.tbl.to_lance()
        df_count = duckdb.sql("SELECT COUNT(*) FROM lance_tbl").to_df()
        return df_count.iloc[0]["count_star()"]

    def search_by_image(self, image: Image, limit: int) -> pd.DataFrame:
        df_hits = (
            self.tbl.search(self.model.embed_image(image=image)).limit(limit).to_df()
        )
        return df_hits

    def search_by_image_path(self, image_path: str, limit: int) -> pd.DataFrame:
        df_hits = (
            self.tbl.search(self.model.embed_image(image_path=image_path))
            .limit(limit)
            .to_df()
        )
        return df_hits

    def search_by_text(self, query_string: str, limit: int) -> pd.DataFrame:
        df_hits = (
            self.tbl.search(self.model.embed_text(query=query_string))
            .limit(limit)
            .to_df()
        )
        return df_hits
