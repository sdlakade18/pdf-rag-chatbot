import chromadb
from app.core.config import settings

class ChromaStore:
    def __init__(self, persist_directory: str | None = None):
        persist_directory = persist_directory or settings.CHROMA_PATH
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name="pdf_documents"
        )

    def add_chunks(
        self,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict]
    ):
        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search( self,
    query_embedding: list[float],
    document_id: str,
    top_k: int = 3):
        return self.collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={
            "document_id": document_id
        }
    )