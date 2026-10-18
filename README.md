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
## Architecture

The project uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions from uploaded PDF documents.

### AWS Workflow

1. **Amazon S3:** Stores uploaded PDF documents.
2. **AWS Lambda:** Triggered when a new PDF is uploaded to the configured S3 bucket.
3. **FastAPI on Amazon EC2:** Receives the PDF from Lambda through an internal API endpoint.
4. **PyMuPDF:** Extracts text from the PDF.
5. **ChromaDB:** Stores document chunks and their vector embeddings for semantic retrieval.
6. **Gemini API:** Generates answers using the retrieved document context.
7. **Amazon CloudWatch:** Collects application and Lambda logs for troubleshooting.

### Technology Stack

- **Backend:** Python, FastAPI
- **Document processing:** PyMuPDF
- **Vector database:** ChromaDB
- **Embeddings:** Sentence Transformers
- **LLM:** Google Gemini API
- **Containerization:** Docker
- **Cloud infrastructure:** Amazon EC2, Amazon S3, AWS Lambda, Amazon ECR
- **Monitoring:** Amazon CloudWatch
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
> **Dependency setup:** The local Python installation instructions are being finalized. The Docker build currently expects a root-level `requirements.txt`; verify that this file is present before building the image.
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

**Dependency setup:** This project includes AWS-specific dependency configuration in `requirements-aws.txt` and `Dockerfile.aws`. The standard `Dockerfile` references `requirements.txt`, which must be present before using that build configuration. Verify the appropriate dependency file and Dockerfile before building an image.

## AWS Deployment Workflow

The application uses an event-driven workflow to process PDF documents stored in Amazon S3.

1. **Upload:** A PDF is uploaded to the configured S3 bucket.
2. **Trigger:** An S3 object-created event invokes the `pdf-rag-s3-processor` Lambda function for matching PDF files.
3. **Download:** Lambda retrieves the PDF from S3.
4. **API request:** Lambda sends the PDF as a multipart upload to the FastAPI backend running on Amazon EC2.
5. **Ingestion:** The backend extracts document text, creates chunks and embeddings, and stores them in ChromaDB.
6. **Question answering:** Users submit questions to the RAG API, which retrieves relevant document context and uses the Gemini API to generate an answer.
7. **Monitoring:** Amazon CloudWatch collects application and Lambda logs for troubleshooting.

### Security Controls

- Restrict inbound EC2 access to trusted IP addresses and the Lambda security group.
- Use an IAM policy scoped to the project S3 bucket for Lambda access.
- Keep API keys and credentials out of source control.
- Review AWS billing and stop unused compute resources when appropriate.

## Testing the API

### 1. Open API Documentation

When the backend is running and reachable, open:

```text
http://localhost:8000/docs
```

For a deployed instance, use the configured API host instead of `localhost`.

### 2. Upload a PDF

In Swagger UI:

1. Find `POST /documents/upload`.
2. Select **Try it out**.
3. Choose a PDF file in the `file` field.
4. Click **Execute**.
5. Verify that the request succeeds.

### 3. Test Question Answering

Use the question-answering endpoint exposed in Swagger UI to submit a question about the uploaded document. Verify that the response is relevant to the PDF content.

### Expected Result

The PDF should be ingested successfully, and questions about its content should receive answers grounded in the retrieved document context.

## Limitations and Cost Management

### Current Limitations

- The API should remain restricted to authorized clients.
- The quality of generated answers depends on PDF text extraction, chunking, retrieval relevance, and the language model.
- Scanned PDFs may require OCR if they do not contain extractable text.
- ChromaDB persistence and document storage must be managed carefully to preserve ingested data.
- Production use requires additional hardening, including authentication, HTTPS, and appropriate request limits.

### AWS Cost Management

The project uses AWS services that may incur charges depending on resource configuration and usage.

- **Amazon EC2:** Stop the instance when the backend is not needed. Attached EBS volumes may continue to incur charges.
- **Amazon ECR:** Review stored container images and remove only images that are no longer required.
- **Amazon S3:** Monitor document storage and request usage.
- **Amazon CloudWatch:** Review log ingestion and retention settings.
- **AWS Lambda:** Monitor invocation counts and execution duration.

Review the AWS Billing and Cost Management dashboard regularly. Stopping EC2 does not eliminate all possible AWS charges.

### Future Improvements

- Add authentication and HTTPS.
- Implement automated testing and CI/CD.
- Add OCR support for scanned PDFs.
- Improve retrieval evaluation and answer-quality monitoring.
- Define suitable CloudWatch log retention policies.


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
