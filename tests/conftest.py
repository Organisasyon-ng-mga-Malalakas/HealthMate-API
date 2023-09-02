import pytest
from sqlalchemy import Sequence, create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import settings
from app.database import Base

Session = scoped_session(sessionmaker())


@pytest.fixture(scope="function")
def dbsession():
    """Returns a DB temporary"""

    engine = create_engine(
        url=f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:"
        f"{settings.DB_PORT}/{settings.DB_DATABASE_TESTING}",
    )
    connection = engine.connect()
    transaction = connection.begin()

    Session.configure(bind=connection)
    Base.metadata.create_all(engine)
    yield Session

    Session.remove()
    transaction.rollback()
    connection.close()
