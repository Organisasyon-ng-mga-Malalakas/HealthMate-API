from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

import app.api.user.controller as user_controller
from app.database import get_db

from .controller import get_user_qnas, upsert_user_qnas
from .schemas import Question, UpsertQuestions

router = APIRouter()


@router.post("/", response_model=dict[str, str])
async def upsert_questions(
    data: UpsertQuestions, db: Session = Depends(get_db)
):
    db_user = user_controller.get_user_by_id(db, id=data.user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Account not found.")

    upsert_user_qnas(db, db_user.id, data.questions)

    return {"status": "ok"}


@router.get("/", response_model=List[Question])
async def read_user_questions(user_id: str, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_id(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Account not found.")

    return get_user_qnas(db, user_id)
