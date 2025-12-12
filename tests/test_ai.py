import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile", 
    api_key=os.getenv("GROQ_API_KEY")
)

try:
    response = llm.invoke("Menga Python haqida 1 ta qiziqarli fakt ayt.")
    print(f"AI Javobi: {response.content}")
except Exception as e:
    print(f"Xatolik yuz berdi: {e}")