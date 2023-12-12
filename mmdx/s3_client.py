from typing import Any, List
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
from io import BytesIO

class S3Client:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str):
        self.aws_access_key_id = access_key
        self.aws_secret_access_key = secret_key
        self.aws_endpoint_url = endpoint_url
        self.client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
        )

    def check_obj_exists(self, bucket: str, file_path: str) -> bool:
        try:
            self.client.head_object(Bucket=bucket, Key=file_path)
            return True
        except self.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise

    def list_objects_names(self, bucket: str) -> List[str]:
        objects = self.client.list_objects_v2(Bucket=bucket)
        file_names = [obj['Key'] for obj in objects.get('Contents', [])]
        return file_names

    def put_obj(self, obj: Any, file_name: str, bucket: str):
        try:
            # Serialize the object (e.g., DataFrame) to bytes
            obj_bytes = BytesIO()
            pd.to_pickle(obj, obj_bytes)
            obj_bytes.seek(0)

            self.client.upload_fileobj(obj_bytes, bucket, file_name)
        except NoCredentialsError:
            print("No AWS credentials found.")

    def get_obj(self, bucket: str, file_name: str):
        response = self.client.get_object(Bucket=bucket, Key=file_name)
        data = response['Body'].read()
        return BytesIO(data)

    def read_csv(self, bucket: str, file_name: str) -> pd.DataFrame:
        response = self.client.get_object(Bucket=bucket, Key=file_name)
        data = response['Body'].read()
        df = pd.read_csv(BytesIO(data))
        return df
