import boto3
import os
from app.config import settings


class S3Service:

    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )

    def download_pdf(self):
        local_path = "data/circle_rates.pdf"
        os.makedirs("data", exist_ok=True)
        self.client.download_file(
            settings.AWS_BUCKET_NAME,
            settings.S3_FILE_KEY,
            local_path
        )
        return local_path


s3_service = S3Service()