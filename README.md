# 📄 PDF RAG Chatbot

> A production-oriented Retrieval-Augmented Generation (RAG) application that lets users upload PDF documents and ask questions grounded in their content.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange)
![Gemini](https://img.shields.io/badge/Gemini-LLM-4285F4?logo=google&logoColor=white)

## 🚀 Overview

This project is a PDF question-answering system built using the **RAG architecture**.

Instead of sending an entire PDF directly to an LLM, the application:

1. Extracts text from the uploaded PDF.
2. Splits the text into smaller chunks.
3. Converts chunks into vector embeddings.
4. Stores embeddings and metadata in ChromaDB.
5. Converts the user's question into an embedding.
6. Retrieves the most relevant chunks from the selected document.
7. Builds a grounded prompt using the retrieved context.
8. Sends the context and question to Gemini.
9. Returns the answer with page/chunk sources.

## ✨ Features

- 📤 PDF upload through a web UI
- 🔎 Semantic search using vector embeddings
- 🧠 Retrieval-Augmented Generation with Gemini
- 🗃️ Persistent ChromaDB vector storage
- 🆔 Document-level retrieval using `document_id`
- 📚 Page and chunk source references
- 💬 Chat-style Streamlit interface
- ⚡ FastAPI backend
- 🔐 API key via environment variables
- 🧩 Modular project structure
- 🧪 Designed for testing and RAG evaluation
- 🐳 Docker-ready architecture

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Streamlit       │
                         │     Frontend        │
                         └──────────┬──────────┘
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                 PDF path                       Question path
                    │                                │
                    ▼                                ▼
                PyMuPDF                         Embedding
                    │                                │
                    ▼                                ▼
                Chunking                         ChromaDB
                    │                         Semantic Search
                    ▼                                │
               Embeddings                             │
                    │                                ▼
                    ▼                         Relevant Chunks
               ChromaDB                              │
                                                     ▼
                                               Prompt Builder
                                                     │
                                                     ▼
                                                   Gemini
                                                     │
                                                     ▼
                                                  Answer
                                                     │
                                                     ▼
                                                Streamlit
```

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application language |
| **PyMuPDF** | PDF text extraction |
| **Sentence Transformers** | Text embeddings |
| **ChromaDB** | Vector database and retrieval |
| **Gemini** | LLM answer generation |
| **FastAPI** | Backend REST API |
| **Streamlit** | Frontend UI |
| **Requests** | Frontend → backend communication |
| **python-dotenv** | Environment variable management |
| **LangChain** | Planned orchestration/refactoring layer |
| **Docker** | Planned containerization |

## 📁 Project Structure

```text
pdf-rag-chatbot/
│
├── app/
│   ├── api/
│   │   └── main.py
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   └── ingest.py
│   ├── vectorstore/
│   │   └── chroma_store.py
│   ├── rag/
│   │   ├── prompt_builder.py
│   │   └── pipeline.py
│   └── llm/
│       └── gemini.py
│
├── frontend/
│   └── app.py
├── documents/
├── data/
│   ├── chroma/
│   └── uploads/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> Local PDFs, uploaded files, ChromaDB data, virtual environments, and secrets should not be committed to Git.

## 🔄 How RAG Works

### Document ingestion

```text
PDF → PyMuPDF → Chunks → Embeddings → ChromaDB
```

Each chunk carries metadata such as:

```python
{
    "document_id": "...",
    "page_number": 1,
    "chunk_id": 7
}
```

### Question answering

```text
Question
   ↓
Query embedding
   ↓
ChromaDB search
   ↓
Filter by document_id
   ↓
Top-K relevant chunks
   ↓
Context + Question
   ↓
Gemini
   ↓
Grounded Answer
```

### Grounded behavior

The prompt instructs Gemini to answer using only the retrieved context.

For example, asking:

```text
What is the capital of France?
```

when the uploaded document contains no such information should produce:

```text
I don't know based on the provided document.
```

rather than an invented document-based answer.

## 🔌 API Endpoints

### `GET /`

Basic API health check.

### `POST /documents/upload`

Uploads and processes a PDF.

Example response:

```json
{
  "document_id": "abc-123",
  "filename": "document.pdf",
  "content_type": "application/pdf",
  "chunks_stored": 10
}
```

### `POST /ask`

Ask a question about a specific uploaded document.

Request:

```json
{
  "question": "What is a Python function?",
  "document_id": "abc-123"
}
```

Response:

```json
{
  "answer": "A function is a reusable block of code...",
  "sources": [
    {
      "page_number": 1,
      "chunk_id": 7
    }
  ]
}
```

## ⚙️ Local Setup

### 1. Clone

```bash
git clone https://github.com/<your-username>/pdf-rag-chatbot.git
cd pdf-rag-chatbot
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini

Create `.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

**Never commit `.env` or expose your API key.**

### 5. Start FastAPI

```bash
uvicorn app.api.main:app --reload
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### 6. Start Streamlit

In a second terminal:

```bash
streamlit run frontend/app.py
```

## 🧪 Example

Upload a PDF and ask:

```text
What is a Python function?
```

The system retrieves relevant chunks and generates a grounded answer while showing the source page/chunk references.

## 🧠 Key Design Decisions

### Why RAG?

RAG retrieves relevant information before generation instead of relying only on the model's general knowledge.

Benefits:

- Better grounding
- Smaller prompts
- Source attribution
- Better scalability for larger documents
- Reduced unsupported answers

### Why FastAPI + Streamlit?

The application separates:

```text
Streamlit → presentation
FastAPI   → application/RAG logic
```

This keeps the RAG pipeline independently testable and allows another client to consume the backend later.

### Why metadata filtering?

Multiple PDFs can exist in the vector store. `document_id` ensures that a question searches the intended document rather than unrelated uploads.

## 📌 Current Status

### Completed

- [x] PDF text extraction
- [x] Basic chunking with overlap
- [x] Sentence Transformer embeddings
- [x] ChromaDB storage
- [x] Semantic retrieval
- [x] Gemini integration
- [x] Grounded RAG pipeline
- [x] Source metadata
- [x] FastAPI backend
- [x] PDF upload endpoint
- [x] Document IDs
- [x] Document-specific retrieval
- [x] Streamlit frontend
- [x] Chat-style interface

### Production hardening

- [ ] Robust input validation
- [ ] File size/type limits
- [ ] Better exception handling
- [ ] Structured logging
- [ ] Idempotent ingestion / upsert strategy
- [ ] Configuration management
- [ ] Automated tests
- [ ] RAG evaluation dataset and metrics
- [ ] Docker containerization
- [ ] Deployment
- [ ] CI/CD

## 🗺️ Roadmap

### Phase 1 — Core RAG
PDF ingestion → chunking → embeddings → vector search → LLM generation

### Phase 2 — Backend & UI
FastAPI → Streamlit → document IDs → source references

### Phase 3 — Productionization
Validation → error handling → logging → configuration → testing → Docker

### Phase 4 — Advanced RAG

Future improvements:

- Better semantic/sentence-aware chunking
- Chunk-size experiments
- Retrieval evaluation
- Reranking
- Hybrid search
- Conversation history
- Multi-document workflows

## 🔐 Security

Do not commit:

```text
.env
venv/
.venv/
data/uploads/
data/chroma/
*.log
```

Never commit:

```env
GEMINI_API_KEY=...
```

Use environment variables and your deployment platform's secret-management system.

## 🎯 Learning Goals

This project demonstrates practical work with:

- Python application architecture
- File handling
- PDF processing
- Text chunking
- Embeddings
- Vector databases
- Semantic search
- RAG architecture
- Prompt engineering
- LLM APIs
- FastAPI
- Streamlit
- API communication
- Error handling
- Testing
- RAG evaluation
- Docker
- Deployment

## 👨‍💻 Author

**Sojwal**  
IT Engineer | AI/ML & Generative AI Projects

---

⭐ If you find this project useful, consider giving the repository a star.
