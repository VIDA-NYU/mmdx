import os
import lancedb
import pandas as pd
import pyarrow as pa
from typing import Iterator
import random
import tqdm
from .model import BaseEmbeddingModel
from .settings import DB_BATCH_SIZE, DATA_SAMPLE_SIZE


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


def load_df(
        db: lancedb.DBConnection, table_name: str, data_path: str, model: BaseEmbeddingModel
) -> lancedb.table.Table:
    return db.create_table(table_name, data=make_df(data_path, model))

