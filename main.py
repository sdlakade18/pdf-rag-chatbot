from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import create_chunks


pages = load_pdf("documents/rag_practice_document.pdf")

for page in pages:

    chunks = create_chunks(
        page["text"],
        page_number=page["page_number"],
        chunk_size=200,
        overlap=50
    )

    for chunk in chunks:
        print(
            f"Page: {chunk['page_number']} | "
            f"Chunk: {chunk['chunk_id']}"
        )
        print(chunk["text"])
        print("-" * 50)