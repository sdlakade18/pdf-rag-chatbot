from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.ingestion.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore


def ingest_pdf(pdf_path: str,document_id: str,embedder: Embedder , store: ChromaStore ):

    # 1. Load PDF
    pages = load_pdf(pdf_path)

    all_chunks = []

    # 3. Create chunks
    for page in pages:

        chunks = create_chunks(
            page["text"],
            page_number=page["page_number"],
            chunk_size=200,
            overlap=50
        )

        all_chunks.extend(chunks)

    # 4. Extract texts
    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    # 5. Create embeddings
    embeddings = embedder.embed_texts(texts)

    # 6. Create IDs
    ids = [
        f"{document_id}_page_{chunk['page_number']}_chunk_{chunk['chunk_id']}"
        for chunk in all_chunks
    ]

    # 7. Create metadata
    metadatas = [
        {   "document_id": document_id,
            "page_number": chunk["page_number"],
            "chunk_id": chunk["chunk_id"]
        }
        for chunk in all_chunks
    ]

    # 8. Store in ChromaDB
    store.add_chunks(
        ids=ids,
        texts=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return {
        "chunks_stored": len(all_chunks)
    }