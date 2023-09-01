from sqlalchemy import Column, DateTime, Text, String, UUID

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, unique=True, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    username = Column(Text, unique=True, nullable=False)
    email = Column(Text, primary_key=True, unique=True, nullable=False)
    password = Column(Text, nullable=False)


