from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

import app.api.user.controller as user_controller
from app.database import get_db

from .controller import get_user_schedules, upsert_user_schedules
from .schemas import Schedule, UpsertSchedules

router = APIRouter()


@router.post("/", response_model=dict[str, str])
async def upsert_schedules(
    data: UpsertSchedules, db: Session = Depends(get_db)
):
    db_user = user_controller.get_user_by_id(db, id=data.user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Account not found.")

    upsert_user_schedules(db, db_user.id, data.schedules)

    return {"status": "ok"}


@router.get("/", response_model=List[Schedule])
async def read_user_schedules(user_id: str, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_id(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Account not found.")

    return get_user_schedules(db, user_id)
