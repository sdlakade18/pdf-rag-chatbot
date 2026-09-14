from app.rag.pipeline import RAGPipeline


rag = RAGPipeline()


question = "What is a Python function?"


result = rag.ask(question)

print("Question:")
print(question)

print("\nAnswer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(
        f"Page {source['page_number']}, "
        f"Chunk {source['chunk_id']}"
    )