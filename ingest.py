from app.ingestion.embedder import Embedder
from app.ingestion.pdf_loader import load_pdf
from app.vectorstore.chroma_store import ChromaStore
from app.ingestion.chunker import create_chunks

pdf_path = "documents/rag_practice_document.pdf"

pages = load_pdf(pdf_path)

embedder = Embedder()
store = ChromaStore()

all_chunks = []
for page in pages:
    chunks = create_chunks(page["text"], chunk_size=200, page_number=page["page_number"], overlap=50)
    all_chunks.extend(chunks)

texts = [chunk["text"] for chunk in all_chunks]

embeddings = embedder.embed_texts(texts)

ids = [f"practice_pdf_page_{chunk['page_number']}_chunk_{chunk['chunk_id']}" for chunk in all_chunks]

metadatas = [{"page_number": chunk["page_number"], "chunk_id": chunk["chunk_id"]} for chunk in all_chunks]

store.add_chunks(ids=ids, texts=texts, embeddings=embeddings, metadatas=metadatas)

print(f"Stored {len(all_chunks)} chunks in ChromaStore.")