import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain va RAG kutubxonalari
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# .env yuklaymiz
load_dotenv()

app = FastAPI(title="Smart RAG Assistant", version="1.0")

# --- SOZLAMALAR ---
CONNECTION_STRING = "postgresql+psycopg2://postgres:1234@127.0.0.1:5433/rag_db"
# Model nomi .env da bo'lmasa, shu yerdan oladi
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile") 

# 1. Embedding Model (Lokal)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Vektor Baza bilan ulanish
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_docs",
    connection=CONNECTION_STRING,
    use_jsonb=True,
)

# 3. LLM (Groq)
llm = ChatGroq(
    temperature=0, 
    model_name=GROQ_MODEL_NAME, 
    api_key=os.getenv("GROQ_API_KEY")
)

# --- Pydantic Modellar ---
class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = [] # Qaysi matndan olganini ko'rsatish uchun

# --- ENDPOINTLAR ---

@app.get("/")
def read_root():
    return {"message": "Smart RAG API ishlamoqda! Docs uchun /docs ga boring."}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    PDF faylni yuklaydi, maydalaydi va Vektor Bazaga saqlaydi.
    """
    try:
        # 1. Faylni vaqtincha saqlab turamiz (chunki PyPDFLoader fayl yo'lini so'raydi)
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. PDFni o'qiymiz
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # 3. Maydalaymiz (Chunking)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        # 4. Bazaga yozamiz
        vector_store.add_documents(chunks)

        # 5. Vaqtincha faylni o'chiramiz
        os.remove(file_path)

        return {"message": f"{len(chunks)} ta bo'lakka bo'linib, bazaga saqlandi! ✅"}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Foydalanuvchi savoliga bazadan javob qidiradi.
    """
    try:
        # 1. Bazadan o'xshash joylarni qidirish
        docs = vector_store.similarity_search(request.question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        if not context:
            return {"answer": "Kechirasiz, hujjatlarda bu haqida ma'lumot topilmadi.", "sources": []}

        # 2. Prompt
        template = """
        Quyidagi kontekstga asoslanib savolga javob ber. 
        Agar javob kontekstda bo'lmasa, "Bilmayman" deb javob ber.
        
        Kontekst: {context}
        
        Savol: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm

        # 3. AI Javobi
        response = chain.invoke({"context": context, "question": request.question})
        
        return {
            "answer": response.content,
            "sources": [doc.page_content[:100] + "..." for doc in docs] # Manbani qisqacha ko'rsatish
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))