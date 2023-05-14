from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Define schemas
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: str
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass