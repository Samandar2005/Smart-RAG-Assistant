import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

CONNECTION_STRING = "postgresql+psycopg2://user:password@localhost:5433/rag_db"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 1. Bazani qayta ulaymiz
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_docs",
    connection=CONNECTION_STRING,
    use_jsonb=True,
)

# 2. Groq (LLM)
llm = ChatGroq(
    temperature=0, 
    model_name=os.getenv("GROQ_MODEL"), # Model nomini .env dan oladi
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_question(question):
    # A) Bazadan o'xshash joylarni qidiramiz (similarity search)
    docs = vector_store.similarity_search(question, k=3) # Eng o'xshash 3 ta joy
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # B) Prompt tayyorlaymiz
    template = """
    Quyidagi kontekstga asoslanib savolga javob ber. 
    O'zingdan to'qima, faqat kontekstda bor narsani ayt.
    
    Kontekst: {context}
    
    Savol: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    # C) Javob olamiz
    response = chain.invoke({"context": context, "question": question})
    return response.content

# Sinov
if __name__ == "__main__":
    savol = input("Savol bering: ")
    javob = ask_question(savol)
    print("\nJavob:", javob)