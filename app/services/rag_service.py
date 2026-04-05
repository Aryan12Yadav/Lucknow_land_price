from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from openai import OpenAI
from app.config import settings
from typing import List


# Custom Embedding Class
class NvidiaEmbeddings(Embeddings):

    def __init__(self):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=settings.NVIDIA_API_KEY
        )
        self.model = "nvidia/nv-embedqa-e5-v5"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Plain strings directly bhejo - no tokenization
        embeddings = []
        for text in texts:
            text = text.replace("\n", " ").strip()
            response = self.client.embeddings.create(
                input=[text],
                model=self.model,
                encoding_format="float",
                extra_body={"input_type": "passage"}
            )
            embeddings.append(response.data[0].embedding)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        text = text.replace("\n", " ").strip()
        response = self.client.embeddings.create(
            input=[text],
            model=self.model,
            encoding_format="float",
            extra_body={"input_type": "query"}
        )
        return response.data[0].embedding


class RAGService:

    def __init__(self):
        self._embedding = None
        self.vectorstore = None
        self.retriever = None

    @property
    def embedding(self):
        if self._embedding is None:
            print("Loading embedding via NVIDIA API...")
            self._embedding = NvidiaEmbeddings()
        return self._embedding

    def load_pdf(self, file_path: str):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50
        )
        return splitter.split_documents(documents)

    def build_vectorstore(self, file_path: str):
        docs = self.load_pdf(file_path)
        self.vectorstore = FAISS.from_documents(docs, self.embedding)
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )

    def search(self, query: str):
        if not self.retriever:
            raise ValueError("Vector store not built")
        results = self.retriever.invoke(query)
        return [doc.page_content for doc in results]

    def save_vectorstore(self, path="faiss_index"):
        if self.vectorstore is None:
            raise ValueError("Vectorstore not built")
        self.vectorstore.save_local(path)

    def load_vectorstore(self, path="faiss_index"):
        self.vectorstore = FAISS.load_local(
            path,
            self.embedding,
            allow_dangerous_deserialization=True
        )
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )


rag_service = RAGService()