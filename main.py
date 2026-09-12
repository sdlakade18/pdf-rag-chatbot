from app.ingestion.ingest import ingest_pdf

result = ingest_pdf(
    "documents/rag_practice_document.pdf",
    "doc_test_001"
)

print(result)