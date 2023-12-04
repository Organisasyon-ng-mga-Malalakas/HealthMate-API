from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, UUID4


# Define schemas
class UserBase(BaseModel):
    username: str
    email: str
    birthdate: datetime = None
    gender: str = None


class UserCreate(UserBase):
    id: Optional[UUID4]
    password: str


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: UUID4
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass