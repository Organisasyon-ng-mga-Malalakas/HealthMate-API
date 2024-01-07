from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

import app.api.user.controller as user_controller
from app.database import get_db

from .controller import (
    get_user_inventory,
    upsert_user_inventory,
    delete_inventory_item,
)
from .schemas import Inventory, UpsertInventory

router = APIRouter()


@router.post("/", response_model=dict[str, str])
async def upsert_inventory(
    data: UpsertInventory, db: Session = Depends(get_db)
):
    db_user = user_controller.get_user_by_id(db, id=data.user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Account not found.")

    upsert_user_inventory(db, db_user.id, data.inventory)

    return {"status": "ok"}


@router.get("/", response_model=List[Inventory])
async def read_user_inventory(user_id: str, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_id(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Account not found.")

    return get_user_inventory(db, user_id)


@router.delete("/", response_model=dict[str, str])
async def delete_inventory(id: str, db: Session = Depends(get_db)):
    is_ok = delete_inventory_item(db, id)
    if not is_ok:
        raise HTTPException(status_code=500, detail="Unable to delete item.")

    return {"status": "ok"}
