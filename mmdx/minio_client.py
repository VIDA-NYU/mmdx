from typing import Any, Optional, List
import pandas as pd
from minio import Minio
from io import BytesIO
from minio.error import S3Error
import pickle
import yaml


class MinioClient:
    def __init__(self, access_key: str, secret_access_key: str, minio_endpoint):
        self.access_key = access_key
        self.secret_key = secret_access_key
        self.minio_endpoint = minio_endpoint
        self.client = Minio(
            self.minio_endpoint,
            access_key=access_key,
            secret_key=secret_access_key,
            secure=False,
        )

    def get_storage_options(self) -> dict:
        return {
            "key": self.access_key,
            "secret": self.secret_key,
            "endpoint_url": self.config.get("minio_endpoint_url"),
        }

    def put_obj(self, obj: Any, file_name: str, bucket: str):
        raise NotImplementedError

    def get_obj(self, bucket: str, file_name: str):
        obj = self.client.get_object(bucket, file_name)
        return obj

    def read_csv(self, bucket: str, file_name: str) -> pd.DataFrame:
        df = pd.read_csv(
            f"s3://{bucket}/{file_name}", storage_options=self.get_storage_options
        )
        return df

    def read_df_parquet(self, bucket: str, file_name: str) -> pd.DataFrame:
        df = pd.read_parquet(
            f"s3://{bucket}/{file_name}", storage_options=self.get_storage_options()
        )
        return df

    def save_df_parquet(self, bucket: str, file_name: str, df: pd.DataFrame) -> None:
        file_name = f"s3://{bucket}/{file_name}.parquet"
        storage = self.get_storage_options()
        df.to_parquet(file_name, index=False, storage_options=storage)
        print(f"{file_name} saved on bucket {bucket}")

    def store_image(self, image: Any, file_name: str, length: int, bucket_name: str):
        self.client.put_object(
            bucket_name,
            file_name,
            data=image,
            length=length,
        )

    def check_obj_exists(self, bucket: str, file_path: str):
        try:
            return self.client.stat_object(bucket, file_path) is not None
        except (S3Error, ValueError) as err:
            if "empty bucket name" in str(err):
                # Object doesn't exist or empty bucket name error
                return False
            if isinstance(err, S3Error) and err.code == "NoSuchKey":
                # Object doesn't exist
                return False

    def list_objects_names(self, bucket: str) -> List[str]:
        objects = self.client.list_objects(bucket, recursive=True)
        file_names = []
        for obj in objects:
            file_names.append(obj.object_name)
        return file_names
