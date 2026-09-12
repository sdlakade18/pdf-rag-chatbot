def build_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for document, metadata in zip(documents, metadatas):

        page_number = metadata["page_number"]
        chunk_id = metadata["chunk_id"]

        context_parts.append(
            f"[Page {page_number}, Chunk {chunk_id}]\n"
            f"{document}"
        )

    return "\n\n".join(context_parts)

def build_prompt(context: str, question: str) -> str:
    return f"""
You are a helpful assistant answering questions about a document.

Answer the question using only the provided context.

Rules:
- Do not use information that is not present in the context.
- Do not make up or assume information.
- If the answer cannot be found in the context, say:
  "I don't know based on the provided document."

Context:
{context}

Question:
{question}

Answer:
"""