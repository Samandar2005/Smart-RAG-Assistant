import shutil
import os
from fastapi import UploadFile
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings


def get_embeddings():
    """Matnni vektorga aylantiruvchi model"""
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

def get_vector_store():
    """PostgreSQL bilan bog'lanish"""
    embeddings = get_embeddings()
    return PGVector(
        embeddings=embeddings,
        collection_name="my_docs",
        connection=settings.DATABASE_URL,
        use_jsonb=True,
    )

def get_llm():
    """Groq AI modelini qaytaradi"""
    return ChatGroq(
        temperature=0, 
        model_name=settings.GROQ_MODEL, 
        api_key=settings.GROQ_API_KEY
    )


def process_and_save_pdf(file: UploadFile):
    """
    UploadedFile ni oladi -> Temp saqlaydi -> Chunk qiladi -> Bazaga yozadi
    """
    try:
        temp_filename = f"temp_{file.filename}"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        loader = PyPDFLoader(temp_filename)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        vector_store = get_vector_store()
        vector_store.add_documents(chunks)

        os.remove(temp_filename)

        return len(chunks)
    
    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise e