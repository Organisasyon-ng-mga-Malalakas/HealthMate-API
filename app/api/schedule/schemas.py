from datetime import datetime
from typing import List, Optional

import uuid

from pydantic import BaseModel, UUID4, validator

class Schedule(BaseModel):
    schedule_id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    schedule_state: Optional[int]
    time_to_take: datetime
    notes: Optional[str]
    quantity: float
    image: Optional[str]

    @validator('schedule_id', pre=True)
    def validate_schedule_id(cls, v):
        if not isinstance(v, str):
            if isinstance(v, uuid.UUID):
                return str(v)
        return v

    class Config:
        orm_mode = True

class UpsertSchedules(BaseModel):
    user_id: str
    schedules: list[Schedule]