from app.api.main import QuestionRequest
import pytest


def test_valid_question_request():
    request = QuestionRequest(
        question="What is Python?",
        document_id="abc123"
    )

    assert request.question == "What is Python?"
    assert request.document_id == "abc123"


def test_question_is_trimmed():
    request = QuestionRequest(
        question="   What is Python?   ",
        document_id="abc123"
    )

    assert request.question == "What is Python?"


def test_empty_question_is_rejected():
    with pytest.raises(ValueError):
        QuestionRequest(
            question="   ",
            document_id="abc123"
        )