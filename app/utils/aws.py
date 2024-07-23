import os
import boto3
from mimetypes import guess_type


class S3:
    def __init__(self):
        self.expire_in = 3600  # 1 hour
        self.bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def upload_file(self, file, name: str):
        content_type, _ = guess_type(name)
        content_type = content_type or "application/octet-stream"

        return self.s3_client.put_object(
            Body=file,
            Bucket=self.bucket_name,
            Key=name,  # com
            ContentType=content_type,
        )

    def download_file(self, key):
        return self.s3_client.get_object(Bucket=self.bucket_name, Key=key)

    def get_file_url(self, key):
        return self.s3_client.generate_presigned_url(
            ClientMethod="get_object",
            ExpiresIn=self.expire_in,
            Params={"Bucket": self.bucket_name, "Key": key},
        )
