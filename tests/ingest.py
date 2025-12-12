from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

CONNECTION_STRING = "postgresql+psycopg2://postgres:1234@localhost:5433/rag_db"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def ingest_pdf(pdf_path):
    print("PDF yuklanmoqda...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"{len(chunks)} ta bo'lakka bo'lindi.")

    print("Vektorlar bazaga yozilmoqda...")
    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="my_docs",
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )
    print("Bajarildi! ✅")

if __name__ == "__main__":
    ingest_pdf("namuna_shartnoma.pdf") 