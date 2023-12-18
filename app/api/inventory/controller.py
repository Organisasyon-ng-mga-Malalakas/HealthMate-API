import uuid
from datetime import datetime, timedelta

from pydantic import UUID4
from sqlalchemy import literal
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import Inventory as InventoryModel

from .schemas import Inventory


def get_user_inventory(db: Session, user_id: str):
    return (
        db.query(*InventoryModel.__table__.columns)
        .filter(InventoryModel.user_id == user_id)
        .all()
    )


def upsert_user_inventory(db: Session, user_id: str, inventory: list[Inventory]):
    stmt = insert(InventoryModel).values(
        [
            {
                "created_at": datetime.utcnow(),
                "user_id": user_id,
                **entry.dict(
                    exclude={
                        "created_at",
                        "deleted_at",
                        "updated_at",
                    }
                ),
            }
            for entry in inventory
        ]
    )
    stmt = stmt.on_conflict_do_update(
        constraint="inventory_pkey",
        set_={
            "updated_at": datetime.utcnow(),
            "brand_name": stmt.excluded.brand_name,
            "medicine_name": stmt.excluded.medicine_name,
            "dosage": stmt.excluded.dosage,
            "dosage_unit": stmt.excluded.dosage_unit,
            "stock": stmt.excluded.stock,
            "medication_type": stmt.excluded.medication_type,
            "description": stmt.excluded.description,
        },
    )
    db.execute(stmt)
    db.commit()
