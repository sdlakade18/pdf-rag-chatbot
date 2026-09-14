import json

from app.ingestion.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore


DOCUMENT_ID = "0ebf8948-8565-45b1-95e4-36bd3e9e8e39"
TOP_K = 3


def main():
    with open("evaluation/questions.json", "r", encoding="utf-8") as file:
        questions = json.load(file)

    embedder = Embedder()
    store = ChromaStore()

    hits = 0

    for item in questions:
        question = item["question"]
        expected_chunk = item["expected_chunk"]

        query_embedding = embedder.embed_text(question)

        results = store.search(
            query_embedding=query_embedding,
            document_id=DOCUMENT_ID,
            top_k=TOP_K
        )

        sources = results["metadatas"][0]


        retrieved_chunks = [
            source["chunk_id"]
            for source in sources
        ]

        hit = expected_chunk in retrieved_chunks

        if hit:
            hits += 1

        print(f"\nQuestion: {question}")
        print(f"Expected chunk: {expected_chunk}")
        print(f"Retrieved chunks: {retrieved_chunks}")
        print(f"Result: {'HIT' if hit else 'MISS'}")

    score = hits / len(questions)

    print("\n--------------------")
    print(f"Chunk Retrieval Hit Rate@{TOP_K}: {score:.2%}")
    print("--------------------")


if __name__ == "__main__":
    main()