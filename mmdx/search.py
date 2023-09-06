import os
import lancedb
import pandas as pd
from PIL import Image
import pyarrow as pa
from .model import BaseEmbeddingModel
import duckdb
import pyarrow as pa
from typing import Iterator


BATCH_MODE = False
DEFAULT_TABLE_NAME = "images"
DEFAULT_SCHEMA = pa.schema(
    [
        pa.field("image_path", pa.utf8()),
        pa.field("vector", pa.list_(pa.float32(), 512)),
    ]
)


def find_files_in_path(path, file_extensions=(".png", ".jpg", "jpeg")) -> Iterator[str]:
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith(file_extensions):
                relative_dir = dirpath.replace(path, "")
                file_path = os.path.join(relative_dir, filename)
                print(f"Walking file: {file_path}")
                yield file_path


def create_df(data_path: str, image_paths: list[str], model: BaseEmbeddingModel):
    vectors = []
    for path in image_paths:
        embedding = model.embed_image_path(os.path.join(data_path, path))
        vectors.append(embedding)
    return pd.DataFrame({"image_path": image_paths, "vector": vectors})
    # return pa.RecordBatch.from_arrays(
    #     [
    #         pa.array(vectors),
    #         pa.array(image_paths),
    #     ],
    #     ["vector", "image_path"],
    # )


def make_batches(
    data_path: str, all_files: list[str], model: BaseEmbeddingModel, batch_size=18
) -> pd.DataFrame:
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i : i + batch_size]
        yield create_df(data_path, batch, model)
    # batch = []
    # for file in all_files:
    #     batch.append(file)
    #     if len(batch) == batch_size:
    #         yield create_df(data_path, batch, model)
    #         batch = []
    # if batch:
    #     yield batch


def load_batches(
    db: lancedb.DBConnection, table_name: str, data_path: str, model: BaseEmbeddingModel
):
    # image_files = list(find_files_in_path(data_path))
    # print(f"Found {len(image_files)} files in {data_path}")
    # for b in make_batches(data_path, image_files, model):
    #     print(f"DF:\n {b}")
    # tbl = db.create_table(
    #     DEFAULT_TABLE_NAME,
    #     make_batches(data_path, image_files, model),
    #     schema=DEFAULT_SCHEMA,
    # )
    # tbl.add(make_batches(data_path, model))
    raise NotImplementedError()


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
    print("\n\nDF: ")
    print(df)
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
        data_path: str, db_path: str, model: BaseEmbeddingModel, delete_existing=True
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
            if BATCH_MODE:
                tbl = load_batches(db, table_name, data_path, model)
            else:
                tbl = db.create_table(
                    DEFAULT_TABLE_NAME, data=make_df(data_path, model)
                )
            return VectorDB(db, tbl, model, data_path)

    def count_rows(self) -> pd.DataFrame:
        lance_tbl = self.tbl.to_lance()
        return duckdb.sql("SELECT COUNT(image_path) FROM lance_tbl").to_df()

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
