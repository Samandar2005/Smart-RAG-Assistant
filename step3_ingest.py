from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

# 1. DB ulanish manzili
CONNECTION_STRING = "postgresql+psycopg2://postgres:1234@localhost:5433/rag_db"

# 2. Embedding Model (Kompyuteringizda lokal ishlaydi, internet kerakmas)
# Bu model matnni 384 o'lchamli vektorga aylantiradi
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def ingest_pdf(pdf_path):
    print("PDF yuklanmoqda...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Matnni bo'laklarga bo'lamiz (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"{len(chunks)} ta bo'lakka bo'lindi.")

    # Bazaga yozamiz (Eng muhim joyi!)
    print("Vektorlar bazaga yozilmoqda...")
    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="my_docs",
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )
    print("Bajarildi! ✅")

# Ishlatib ko'rish uchun bitta PDF fayl nomini yozing
if __name__ == "__main__":
    ingest_pdf("namuna_shartnoma.pdf") # O'zingizda bor pdf nomini yozing