from app.ingestion.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore


embedder = Embedder()
store = ChromaStore()

texts = [
    "Python functions are reusable blocks of code.",
    "Python lists store multiple values.",
    "A dictionary stores key-value pairs."
]

embeddings = embedder.embed_texts(texts)

ids = [
    "test_chunk_1",
    "test_chunk_2",
    "test_chunk_3"
]

metadatas = [
    {"page_number": 1},
    {"page_number": 2},
    {"page_number": 3}
]

store.add_chunks(
    ids=ids,
    texts=texts,
    embeddings=embeddings,
    metadatas=metadatas
)

query = "What are Python functions?"

query_embedding = embedder.embed_text(query)

results = store.search(
    query_embedding=query_embedding,
    top_k=2
)

print(results)