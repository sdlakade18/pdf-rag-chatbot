# RAG Evaluation Results

## Dataset

Initial evaluation dataset contains 4 questions based on the practice PDF.

## Retrieval

Metric: Chunk Retrieval Hit@3

Result: 75% (3/4)

| Question | Expected Chunk | Retrieved Chunks | Result |
|---|---:|---|---|
| What is a Python function? | 6 | 7, 1, 6 | HIT |
| What is a Python list? | 4 | 1, 4, 10 | HIT |
| What is a Python dictionary? | 5 | 1, 10, 4 | MISS |
| What is Python used for in AI? | 8 | 7, 8, 1 | HIT |

## End-to-End Answer Evaluation

| Question | Result |
|---|---|
| What is a Python function? | Correct |
| What is a Python list? | Correct |
| What is a Python dictionary? | Abstained due to insufficient retrieved context |
| What is Python used for in AI? | Correct |

End-to-end answer accuracy on this initial dataset: 75%.

## Observations

The dictionary query failed because the relevant chunk was not retrieved in the Top-3 results.

The LLM correctly followed the grounding instruction and returned:

"I don't know based on the provided document."

This indicates a retrieval/chunking limitation rather than a generation hallucination.

## Future Improvements

- Sentence-aware / semantic chunking
- Better chunk overlap
- Explicit cosine similarity configuration
- Retrieval relevance threshold
- Reranking
- Larger evaluation dataset
- Automated faithfulness and answer-relevance evaluation