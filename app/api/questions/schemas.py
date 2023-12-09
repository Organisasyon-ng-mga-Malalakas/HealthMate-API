from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, UUID4

class Question(BaseModel):
    name: str
    category: str
    value: float

    class Config:
        orm_mode = True

class UpsertQuestions(BaseModel):
    user_id: str
    questions: list[Question]