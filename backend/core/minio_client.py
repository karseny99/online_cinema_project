import boto3
from botocore.client import Config

MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "moviess"

class MinioClient:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=f"http://{MINIO_ENDPOINT}",
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            config=Config(signature_version="s3v4"),
        )

    def get_presigned_url(self, object_name):
        """Получение временной ссылки на объект."""
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": object_name + ".mp4"},
            ExpiresIn=3600,  # 1 час
        )

    def upload_file(self, file_path, object_name):
        """Загрузка файла в MinIO."""
        self.client.upload_file(file_path, BUCKET_NAME, object_name)
