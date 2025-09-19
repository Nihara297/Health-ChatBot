from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from typing import List
import os


def get_hugging_face_embeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(model_name=model_name)


def download_embeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Alias for backward compatibility."""
    return HuggingFaceEmbeddings(model_name=model_name)


# ✅ New function with the exact name your app.py expects
def download_hugging_face_embeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Download and return Hugging Face embeddings (same as download_embeddings)."""
    return HuggingFaceEmbeddings(model_name=model_name)


def load_pdf_files(folder_path: str) -> List[Document]:
    loader = DirectoryLoader(folder_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents


def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source", "")
        minimal_docs.append(
            Document(page_content=doc.page_content, metadata={"source": src})
        )
    return minimal_docs


def text_split(minimal_docs: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    return text_splitter.split_documents(minimal_docs)
