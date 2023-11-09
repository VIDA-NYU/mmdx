import os
import lancedb
import pandas as pd
import pyarrow as pa
from typing import Iterator, List, Optional
import random
import tqdm
from .model import BaseEmbeddingModel
from .settings import DB_BATCH_SIZE, DATA_SAMPLE_SIZE, IMAGE_EXTENSIONS
import imghdr
from io import BytesIO
from .minio_client import MinioClient


def detect_image_type(image_path: str) -> Optional[str]:
    return imghdr.what(image_path)


def find_files_in_path(path, file_extensions=IMAGE_EXTENSIONS) -> Iterator[str]:
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            relative_dir = dirpath.replace(path, "")
            file_path = os.path.join(relative_dir, filename)
            if filename.lower().endswith(file_extensions):
                yield file_path
            else:
                absolute_path = os.path.join(dirpath, filename)
                image_type = detect_image_type(absolute_path)
                if f".{image_type}" in file_extensions:
                    yield file_path


def load_images_from_path(data_path: str, sample_size=DATA_SAMPLE_SIZE):
    image_files = list(find_files_in_path(data_path))
    print(f"Found {len(image_files)} images in {data_path}")
    if sample_size is not None:
        print(f"Sampling {sample_size} out of {len(image_files)} images...")
        image_files = random.sample(image_files, sample_size)
    return image_files


def load_images_from_minio(
    data_path: str, minio_client: MinioClient, sample_size=DATA_SAMPLE_SIZE
):
    image_files = minio_client.list_objects_names(data_path)
    print(f"Found {len(image_files)} images in {data_path}")
    if sample_size is not None:
        print(f"Sampling {sample_size} out of {len(image_files)} images...")
        image_files = random.sample(image_files, sample_size)
    return image_files

def embed_image_files(
    model: BaseEmbeddingModel,
    data_path: str,
    image_paths: List[str],
    minio_client: Optional[MinioClient],
):
    embeddings = []
    for path in image_paths:
        try:
            if isinstance(minio_client, MinioClient):
                image_data = minio_client.get_obj(data_path, path)
                image_buffer = BytesIO(image_data.read())
                embedding = model.embed_image_path(image_buffer)
            else:
                embedding = model.embed_image_path(
                    image_path=os.path.join(data_path, path)
                )
            embeddings.append((path, embedding))
        except Exception as e:
            print(f"Failed to create embbeding for image {path}.", e)
            embeddings.append((path, None))
    return embeddings


def load_batches(
    db: lancedb.DBConnection,
    table_name: str,
    data_path: str,
    minio_client: Optional[MinioClient],
    model: BaseEmbeddingModel,
    batch_size=DB_BATCH_SIZE,
) -> lancedb.table.Table:
    if isinstance(minio_client, MinioClient):
        image_files = load_images_from_minio(data_path, minio_client)
    else:
        image_files = load_images_from_path(data_path)

    def make_batches() -> Iterator[pa.RecordBatch]:
        with tqdm.tqdm(total=len(image_files)) as progress_bar:
            for i in range(0, len(image_files), batch_size):
                image_paths = image_files[i : i + batch_size]

                results = embed_image_files(model, data_path, image_paths, minio_client)
                valid_image_paths = [path for path, emb in results if emb is not None]
                valid_embeddings = [emb for path, emb in results if emb is not None]

                image_paths_array = pa.array(valid_image_paths)
                embeddings_array = pa.array(
                    valid_embeddings, pa.list_(pa.float32(), model.dimensions())
                )

                progress_bar.update(len(image_paths))

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


def make_df(
    data_path: str, model: BaseEmbeddingModel, minio_client: Optional[MinioClient]
):
    if minio_client:
        image_files = load_images_from_path(data_path)
    else:
        image_files = load_images_from_path(data_path)

    image_paths = []
    vectors = []
    for image_path in tqdm.tqdm(image_files):
        image_path, embedding = embed_image_files(model, data_path, [image_path])[0]
        if embedding is not None:
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
    db: lancedb.DBConnection,
    table_name: str,
    data_path: str,
    model: BaseEmbeddingModel,
    minio_client: Optional[MinioClient],
) -> lancedb.table.Table:
    return db.create_table(table_name, data=make_df(data_path, model, minio_client))
