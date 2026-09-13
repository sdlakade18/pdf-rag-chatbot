from fastapi import FastAPI
from pydantic import BaseModel
from app.rag.pipeline import RAGPipeline
from fastapi import File, UploadFile
from pathlib import Path
import uuid
from app.ingestion.ingest import ingest_pdf




app= FastAPI(
    title="PDF RAG Chatbot",
    description="A chatbot that can answer questions about PDF documents using a Retrieval-Augmented Generation (RAG) approach.",
    version="1.0.0",
)

rag = RAGPipeline()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str
    document_id: str
    
class Source(BaseModel):
    page_number: int
    chunk_id: int
    
class QuestionResponse(BaseModel):
    answer: str
    sources: list[Source]


@app.get("/")
def root():
    return {"message": "Welcome to the PDF RAG Chatbot API!"}


@app.post("/ask",response_model=QuestionResponse)
@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    result = rag.ask(
        question=request.question,
        document_id=request.document_id
    )
    return result

@app.post("/documents/upload")
def upload_pdf(file: UploadFile = File(...)):

    document_id = str(uuid.uuid4())

    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
        
    result = ingest_pdf(
        pdf_path=str(file_path), 
        document_id=document_id
        )
    

    return {
        "document_id": document_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "chunks_stored": result["chunks_stored"]
    }

