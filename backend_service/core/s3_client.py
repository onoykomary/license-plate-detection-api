import boto3
from aiobotocore.session import get_session
from .config import settings
from contextlib import asynccontextmanager


class BaseS3Config:
    def __init__(self):
        self.bucket = settings.S3_BUCKET_NAME
        self.credentials = {
            "aws_access_key_id": settings.S3_ACCESS_KEY,
            "aws_secret_access_key": settings.S3_SECRET_KEY,
            "endpoint_url": settings.S3_ENDPOINT_URL,
        }


class AsyncS3Client(BaseS3Config):
    def __init__(self):
        super().__init__()
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.credentials) as client:
            yield client

    async def upload_file(self, file: bytes, obj_name: str):
        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket, Key=obj_name, Body=file)
            return obj_name
        
    async def create_bucket_if_not_exists(self):
            async with self.get_client() as client:
                response = await client.list_buckets()
                existing_buckets = [b['Name'] for b in response.get('Buckets', [])]
                
                if self.bucket not in existing_buckets:
                    await client.create_bucket(Bucket=self.bucket)
                    print(f"Bucket {self.bucket} is created.")
                else:
                    print(f"Bucket {self.bucket} exists.")


class SyncS3Client(BaseS3Config):
    def __init__(self):
        super().__init__()
        self.client = boto3.client("s3", **self.credentials)

    def download_file(self, obj_name: str) -> bytes:
        response = self.client.get_object(Bucket=self.bucket, Key=obj_name)
        return response["Body"].read()


async_s3_client = AsyncS3Client()
sync_s3_client = SyncS3Client()
