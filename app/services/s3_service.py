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
        print("PDF downloaded from S3")
        return local_path

    # FAISS index S3 pe save karo
    def upload_faiss(self, local_path="faiss_index"):
        for filename in ["index.faiss", "index.pkl"]:
            self.client.upload_file(
                f"{local_path}/{filename}",
                settings.AWS_BUCKET_NAME,
                f"faiss_index/{filename}"
            )
        print("FAISS index uploaded to S3")

    # FAISS index S3 se download karo
    def download_faiss(self, local_path="faiss_index"):
        os.makedirs(local_path, exist_ok=True)
        for filename in ["index.faiss", "index.pkl"]:
            self.client.download_file(
                settings.AWS_BUCKET_NAME,
                f"faiss_index/{filename}",
                f"{local_path}/{filename}"
            )
        print("FAISS index downloaded from S3")

    # S3 pe FAISS hai ya nahi check karo
    def faiss_exists_on_s3(self):
        try:
            self.client.head_object(
                Bucket=settings.AWS_BUCKET_NAME,
                Key="faiss_index/index.faiss"
            )
            return True
        except:
            return False


s3_service = S3Service()