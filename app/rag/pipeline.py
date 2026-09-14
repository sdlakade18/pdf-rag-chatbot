from app.ingestion.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore
from app.rag.prompt_builder import build_context, build_prompt
from app.llm.gemini import GeminiLLM


class RAGPipeline:

    def __init__(self):
        self.embedder = Embedder()
        self.store = ChromaStore()

        self.llm = GeminiLLM()

    def ask(self, question: str, document_id: str, top_k: int = 3) -> str:

        # 1. Convert question into embedding
        query_embedding = self.embedder.embed_text(question)

        # 2. Retrieve relevant chunks
        results = self.store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            document_id=document_id
        )
        
        if not results["documents"] or not results["documents"][0]:
            return {
            "answer": "I don't know based on the provided document.",
            "sources": []
    }

        # 3. Build context
        context = build_context(results)

        # 4. Build grounded prompt
        prompt = build_prompt(
            context=context,
            question=question
        )

        sources = results["metadatas"][0]
        answer = self.llm.generate(prompt)
        return {
        "answer": answer,
        "sources": sources
    }

