from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException
)
from app.core.config import settings
from pydantic import BaseModel,Field,field_validator
from app.rag.pipeline import RAGPipeline
from fastapi import File, UploadFile
from pathlib import Path
import uuid
from app.ingestion.ingest import ingest_pdf
import fitz, logging
from app.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


app= FastAPI(
    title="PDF RAG Chatbot",
    description="A chatbot that can answer questions about PDF documents using a Retrieval-Augmented Generation (RAG) approach.",
    version="1.0.0",
)

rag = RAGPipeline()
embedder = rag.embedder
store = rag.store

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the document"
    )

    document_id: str = Field(
        ...,
        min_length=1,
        description="ID of the uploaded document"
    )
    
    @field_validator("question")
    @classmethod
    def validate_question(cls, value:str):
        if not value.strip():
            raise ValueError("Question cannot be empty")
        return value.strip()

class Source(BaseModel):
    page_number: int
    chunk_id: int
    
class QuestionResponse(BaseModel):
    answer: str
    sources: list[Source]


@app.get("/")
def root():
    return {"message": "Welcome to the PDF RAG Chatbot API!"}


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):

    logger.info(
        "Question received: document_id=%s",
        request.document_id
    )

    try:
        result = rag.ask(
            question=request.question,
            document_id=request.document_id
        )
    except Exception:
        logger.exception(
            "RAG question failed: document_id=%s",
            request.document_id
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer."
        )

    return result

@app.post("/documents/upload")
def upload_pdf(file: UploadFile = File(...)):
     # 1. Validate filename
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # 2. Read file contents
    contents = file.file.read()

    # 3. Reject empty files
    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # 4. Validate file size
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the {settings.MAX_FILE_SIZE_MB} MB limit."
        )

    # 5. Validate PDF signature
    if not contents.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid PDF."
        )

    # 6. Validate that PyMuPDF can actually open it
    try:
        document = fitz.open(stream=contents, filetype="pdf")
        document.close()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF could not be opened."
        )
    
    document_id = str(uuid.uuid4())
    
    logger.info(
    "Processing PDF: document_id=%s filename=%s",
    document_id,
    file.filename
)

    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    with open(file_path, "wb") as buffer:
        buffer.write(contents)
        
    try:
        result = ingest_pdf(
        pdf_path=str(file_path),
        document_id=document_id,
        embedder=embedder,
        store=store
    )
    except Exception:
        logger.exception(
        "PDF ingestion failed: document_id=%s filename=%s",
        document_id,
        file.filename
    )
        if file_path.exists():
            file_path.unlink()  # Remove the uploaded file if ingestion fails
            logger.info(
                "Removed uploaded file due to ingestion failure: %s",
                document_id
            )

        raise HTTPException(
        status_code=500,
        detail="Failed to process the PDF."
    )
    

    return {
        "document_id": document_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "chunks_stored": result["chunks_stored"]
    }

