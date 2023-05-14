from sqlalchemy import Column, DateTime, Text, String

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String(36), primary_key=True, unique=True, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    username = Column(String(24), unique=True, nullable=False)
    email = Column(String(24), primary_key=True, unique=True, nullable=False)
    password = Column(Text, nullable=False)


