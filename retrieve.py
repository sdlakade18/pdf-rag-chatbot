from app.ingestion.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore


# Create components
embedder = Embedder()
store = ChromaStore()


# Ask a question
query = "What is a Python function?"


# Convert question into an embedding
query_embedding = embedder.embed_text(query)


# Search ChromaDB
results = store.search(
    query_embedding=query_embedding,
    top_k=3
)


# Display retrieved chunks
for i in range(3):

    print(f"\nResult {i + 1}")
    print("-" * 50)

    print("Distance:", results["distances"][0][i])

    print("Metadata:", results["metadatas"][0][i])

    print("Text:")
    print(results["documents"][0][i])