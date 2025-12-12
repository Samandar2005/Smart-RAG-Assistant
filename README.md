# Smart RAG Assistant

A powerful Retrieval-Augmented Generation (RAG) assistant built with FastAPI, LangChain, and Groq AI. This application allows users to upload PDF documents, store them in a vector database, and interact with an AI-powered chatbot that provides context-aware responses based on the uploaded content. Features both a REST API backend and a user-friendly Streamlit web interface.

## Features

- **Document Upload**: Upload PDF files and automatically process them into vector embeddings
- **Vector Search**: Efficient similarity search using PostgreSQL with PGVector
- **AI-Powered Chat**: Conversational interface powered by Groq's Llama models
- **Dual Interface**: Both REST API (FastAPI) and web UI (Streamlit)
- **FastAPI Backend**: RESTful API with automatic documentation
- **Streamlit Frontend**: Intuitive web interface for document upload and chat
- **Local Embeddings**: Uses HuggingFace sentence transformers for privacy and offline capability
- **Docker Support**: Easy deployment with Docker Compose

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Groq API Key (sign up at [groq.com](https://groq.com))

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd smart-rag-assistant
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

3. **Start the database:**
   ```bash
   docker-compose up -d
   ```

4. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install frontend dependencies:**
   ```bash
   cd frontend
   pip install -r requirements.txt
   cd ..
   ```

## Usage

### Running the Backend API

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Running the Web Interface

Start the Streamlit frontend:
```bash
cd frontend
streamlit run app.py
```

The web interface will be available at `http://localhost:8501`

### API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload a PDF document
- `POST /chat` - Ask questions based on uploaded documents

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

### Example Usage

1. Upload a PDF via API:
   ```bash
   curl -X POST "http://localhost:8000/upload" -F "file=@your_document.pdf"
   ```

2. Ask a question via API:
   ```bash
   curl -X POST "http://localhost:8000/chat" \
        -H "Content-Type: application/json" \
        -d '{"question": "What is the main topic of the document?"}'
   ```

3. Or use the web interface: Open `http://localhost:8501` in your browser, upload a PDF, and start chatting!

## Development

The project includes development scripts and tests:

### Scripts
- `step1_test_ai.py` - Test Groq AI connection
- `step3_ingest.py` - Manual PDF ingestion for testing
- `step4_chat.py` - Command-line chat interface

### Tests
- `tests/test_ai.py` - AI functionality tests
- `tests/ingest.py` - Document ingestion tests
- `tests/chat.py` - Chat functionality tests

### Frontend
- `frontend/app.py` - Streamlit web application
- `frontend/requirements.txt` - Frontend dependencies

## Architecture

- **Backend**: FastAPI web framework
- **Frontend**: Streamlit web interface
- **AI Model**: Groq Llama 3.3 70B Versatile
- **Embeddings**: HuggingFace sentence-transformers/all-MiniLM-L6-v2
- **Vector Database**: PostgreSQL with PGVector extension
- **Document Processing**: LangChain for PDF loading and text splitting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain](https://langchain.com/) for the RAG framework
- [Groq](https://groq.com/) for fast AI inference
- [HuggingFace](https://huggingface.co/) for embeddings
- [PGVector](https://github.com/pgvector/pgvector) for vector storage