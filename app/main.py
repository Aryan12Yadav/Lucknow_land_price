from fastapi import FastAPI
from app.routes.chatbot import router as chatbot_router
from app.services.rag_service import rag_service
from app.services.s3_service import s3_service
import os

app = FastAPI()


@app.on_event("startup")
def startup_event():

    print("Starting server...")

    if os.path.exists("faiss_index"):
        print("Loading FAISS index...")
        rag_service.load_vectorstore("faiss_index")

    else:
        print("Downloading PDF from S3...")
        pdf_path = s3_service.download_pdf()

        print("Building FAISS index...")
        rag_service.build_vectorstore(pdf_path)

        rag_service.save_vectorstore("faiss_index")

        print("FAISS index created successfully")

# @app.on_event("startup")
# def startup_event():

#     print("Starting server...")

#     print("Listing S3 files...")
#     s3_service.debug_list_files()

#     exit()  # TEMP stop here

app.include_router(chatbot_router)