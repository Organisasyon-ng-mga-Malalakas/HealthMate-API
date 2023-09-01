from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import (
    declared_attr,
    declarative_base,
)
from sqlalchemy.orm import sessionmaker, Session, as_declarative

from app.core.config import settings

engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
