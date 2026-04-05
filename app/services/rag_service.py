from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

class RAGService:

    def __init__(self):

       
        self.embedding = embedding_model
        self.vectorstore = None
        self.retriever = None

    # -------- PDF → DOCUMENTS --------
    def load_pdf(self, file_path: str):

        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50
        )

        docs = splitter.split_documents(documents)

        return docs

    # -------- BUILD FAISS FROM PDF --------
    def build_vectorstore(self, file_path: str):

        docs = self.load_pdf(file_path)

        self.vectorstore = FAISS.from_documents(
            docs,
            self.embedding
        )
        
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )

    # -------- SEARCH --------
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