from app.rag.prompt_builder import build_context, build_prompt


def test_build_context_contains_source_metadata():
    results = {
        "documents": [["Python is a programming language."]],
        "metadatas": [[
            {
                "page_number": 1,
                "chunk_id": 2
            }
        ]]
    }

    context = build_context(results)

    assert "Page 1, Chunk 2" in context
    assert "Python is a programming language." in context


def test_build_prompt_contains_context_and_question():
    context = "Python is a programming language."
    question = "What is Python?"

    prompt = build_prompt(
        context=context,
        question=question
    )

    assert context in prompt
    assert question in prompt
    assert "Answer the question using only the provided context." in prompt