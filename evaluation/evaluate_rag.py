import json

from app.rag.pipeline import RAGPipeline


DOCUMENT_ID = "0ebf8948-8565-45b1-95e4-36bd3e9e8e39"


def main():
    with open("evaluation/questions.json", "r", encoding="utf-8") as file:
        questions = json.load(file)

    rag = RAGPipeline()

    for item in questions:
        question = item["question"]

        result = rag.ask(
            question=question,
            document_id=DOCUMENT_ID,
            top_k=3
        )

        print("\n" + "=" * 60)
        print(f"Question: {question}")
        print("-" * 60)
        print(f"Answer: {result['answer']}")
        print("-" * 60)
        print("Sources:")

        for source in result["sources"]:
            print(
                f"Page {source['page_number']} | "
                f"Chunk {source['chunk_id']}"
            )


if __name__ == "__main__":
    main()