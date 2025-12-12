import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Smart RAG Assistant"
    PROJECT_VERSION: str = "1.0.0"
    
    DB_USER: str = os.getenv("POSTGRES_USER", "user")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost") 
    DB_PORT: str = os.getenv("DB_PORT", "5433")      
    DB_NAME: str = os.getenv("POSTGRES_DB", "rag_db")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

settings = Settings()