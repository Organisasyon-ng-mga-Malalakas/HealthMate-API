import pytest
from app.api.questions.schemas import Question, UpsertQuestions
from app.api.questions.controller import (upsert_user_qnas, get_user_qnas)



def test_upsert_questions(dbsession):

    user_id = "e6ffd2ee-d8a5-45b4-87c8-db05df9544c2"

    questions = [
        Question(name="test", category="test", value=1),
        Question(name="test", category="test", value=2),
        Question(name="test", category="test", value=3),
    ]

    upsert_user_qnas(dbsession, user_id, questions)

    result = get_user_qnas(dbsession, user_id)

    print(result)