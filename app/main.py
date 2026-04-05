from fastapi import FastAPI
from app.routes.chatbot import router as chatbot_router
from app.services.rag_service import rag_service
from app.services.s3_service import s3_service
import os

app = FastAPI()


@app.on_event("startup")
def startup_event():
    print("Starting server...")

    # Step 1 - Pehle local check karo
    if os.path.exists("faiss_index/index.faiss"):
        print("FAISS index found locally - loading...")
        rag_service.load_vectorstore("faiss_index")
        print("FAISS loaded from local")

    # Step 2 - Local nahi hai, S3 pe check karo
    elif s3_service.faiss_exists_on_s3():
        print("FAISS index found on S3 - downloading...")
        s3_service.download_faiss("faiss_index")
        rag_service.load_vectorstore("faiss_index")
        print("FAISS loaded from S3")

    # Step 3 - Kahin nahi hai, fresh build karo
    else:
        print("No FAISS index found - building from scratch...")
        pdf_path = s3_service.download_pdf()

        print("Building FAISS index...")
        rag_service.build_vectorstore(pdf_path)
        rag_service.save_vectorstore("faiss_index")

        print("Uploading FAISS index to S3...")
        s3_service.upload_faiss("faiss_index")
        print("FAISS index built and saved to S3")


app.include_router(chatbot_router)