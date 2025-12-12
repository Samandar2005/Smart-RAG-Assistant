from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate

from core.config import settings
from core.utils import get_llm, get_vector_store, process_and_save_pdf

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

llm = get_llm()
vector_store = get_vector_store()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []


@app.get("/")
def read_root():
    return {"message": f"{settings.PROJECT_NAME} is running!"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        num_chunks = process_and_save_pdf(file)
        return {"message": f"Muvaffaqiyatli! {num_chunks} ta qism bazaga saqlandi. ✅"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    try:
        docs = vector_store.similarity_search(request.question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        if not context:
            return {"answer": "Hujjatlarda bu haqida ma'lumot topilmadi.", "sources": []}

        template = """
        Quyidagi kontekstga asoslanib savolga javob ber. 
        
        Kontekst: {context}
        
        Savol: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm

        response = chain.invoke({"context": context, "question": request.question})
        
        return {
            "answer": response.content,
            "sources": [doc.page_content[:100] + "..." for doc in docs]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))