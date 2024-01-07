import uuid
from datetime import datetime, timedelta

from pydantic import UUID4
from sqlalchemy import literal
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import Schedule as ScheduleModel

from .schemas import Schedule


def get_user_schedules(db: Session, user_id: str):
    return (
        db.query(*ScheduleModel.__table__.columns)
        .filter(
            ScheduleModel.user_id == user_id, ScheduleModel.deleted_at == None
        )
        .all()
    )


def delete_schedule(db: Session, id: str):
    try:
        (
            db.query(ScheduleModel)
            .filter(ScheduleModel.schedule_id == id)
            .update({ScheduleModel.deleted_at: datetime.utcnow()})
        )

        db.commit()
    except Exception as e:
        print(e)
        return False
    else:
        return True


def upsert_user_schedules(db: Session, user_id: str, schedules: list[Schedule]):
    stmt = insert(ScheduleModel).values(
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
            for entry in schedules
        ]
    )
    stmt = stmt.on_conflict_do_update(
        constraint="schedule_pkey",
        set_={
            "updated_at": datetime.utcnow(),
            "time_to_take": stmt.excluded.time_to_take,
            "inventory_id": stmt.excluded.inventory_id,
            "schedule_state": stmt.excluded.schedule_state,
            "notes": stmt.excluded.notes,
            "quantity": stmt.excluded.quantity,
            "image": stmt.excluded.image,
        },
    )
    db.execute(stmt)
    db.commit()
