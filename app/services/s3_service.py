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

        print("DEBUG BUCKET:", settings.AWS_BUCKET_NAME)
        print("DEBUG KEY:", settings.S3_FILE_KEY)

        self.client.download_file(
            settings.AWS_BUCKET_NAME,
            settings.S3_FILE_KEY,
            local_path
        )

        return local_path
    
    def debug_list_files(self):
        response = self.client.list_objects_v2(
            Bucket=settings.AWS_BUCKET_NAME
        )

        for obj in response.get("Contents", []):
            print("S3 FILE:", obj["Key"])

s3_service = S3Service()
