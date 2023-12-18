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
        .filter(ScheduleModel.user_id == user_id)
        .all()
    )


def upsert_user_schedules(db: Session, user_id: str, schedules: list[Schedule]):
    stmt = insert(ScheduleModel).values(
        [
            {
                "created_at": datetime.utcnow(),
                "schedule_id": str(uuid.uuid4()),
                "user_id": user_id,
                **entry.dict(
                    exclude={
                        "schedule_id",
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
            "schedule_state": stmt.excluded.schedule_state,
            "notes": stmt.excluded.notes,
            "quantity": stmt.excluded.quantity,
            "image": stmt.excluded.image,
        },
    )
    db.execute(stmt)
    db.commit()
