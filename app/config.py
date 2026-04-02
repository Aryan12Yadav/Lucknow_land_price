import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    def __init__(self):
        self.MONGO_URI = os.getenv("MONGO_URI")
        
        self.NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

        self.AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
        self.AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
        self.AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
        self.AWS_REGION = os.getenv("AWS_REGION")
        self.S3_FILE_KEY = os.getenv("S3_FILE_KEY")

        # -------- REQUIRED --------
        if not self.MONGO_URI:
            raise ValueError("MONGO_URI missing in .env")

        if not self.NVIDIA_API_KEY:
            raise ValueError("NVIDIA_API_KEY missing in .env")

        # -------- S3 VALIDATION (IMPORTANT) --------
        if not all([
            self.AWS_ACCESS_KEY,
            self.AWS_SECRET_KEY,
            self.AWS_BUCKET_NAME,
            self.AWS_REGION,
            self.S3_FILE_KEY
        ]):
            raise ValueError("S3 configuration missing in .env")


settings = Settings()