import uuid
from datetime import datetime, timedelta

from pydantic import UUID4
from sqlalchemy import literal
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import Questions

from .schemas import Question, UpsertQuestions


def get_user_qnas(db: Session, user_id: str):
    return db.query(Questions).filter(Questions.user_id == user_id).all()


def upsert_user_qnas(db: Session, user_id: str, questions: list[Question]):
    # ensure no duplicate names
    q_data = { d.name: d for d in questions }
    stmt = insert(Questions).values(
        [
            {
                "created_at": datetime.utcnow(),
                "question_id": str(uuid.uuid4()),
                "user_id": user_id,
                **entry.dict(),
            }
            for entry in q_data.values()
        ]
    )
    stmt = stmt.on_conflict_do_update(
        constraint="questions_pkey",
        set_={"updated_at": datetime.utcnow(), "value": stmt.excluded.value},
    )
    db.execute(stmt)
    db.commit()
