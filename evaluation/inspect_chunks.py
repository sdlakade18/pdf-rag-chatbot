from app.vectorstore.chroma_store import ChromaStore


DOCUMENT_ID = "0ebf8948-8565-45b1-95e4-36bd3e9e8e39"


def main():
    store = ChromaStore()

    results = store.collection.get(
        where={
            "document_id": DOCUMENT_ID
        },
        include=["documents", "metadatas"]
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    for document, metadata in zip(documents, metadatas):
        print("\n" + "=" * 60)

        print(
            f"Page: {metadata['page_number']} | "
            f"Chunk: {metadata['chunk_id']}"
        )

        print("-" * 60)
        print(document)


if __name__ == "__main__":
    main()