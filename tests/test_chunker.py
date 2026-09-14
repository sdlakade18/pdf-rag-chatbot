from app.ingestion.chunker import create_chunks
import pytest

def test_create_chunks_returns_chunks():
    text = "A" * 500

    chunks = create_chunks(
        text=text,
        page_number=1,
        chunk_size=200,
        overlap=50
    )

    assert len(chunks) > 1
    
def test_chunk_contains_page_number():
    text = "A" * 100

    chunks = create_chunks(
        text=text,
        page_number=5,
        chunk_size=200,
        overlap=50
    )

    assert chunks[0]["page_number"] == 5

def test_overlap_must_be_smaller_than_chunk_size():
    text = "A" * 100

    with pytest.raises(ValueError):
        create_chunks(
            text=text,
            page_number=1,
            chunk_size=50,
            overlap=50
        )