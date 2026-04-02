from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/circle_rates.pdf")
docs = loader.load()

print(len(docs))