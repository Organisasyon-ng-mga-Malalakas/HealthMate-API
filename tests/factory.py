from uuid import uuid4

import pytest
from factory import Faker, alchemy, LazyAttribute

from app.models import User

from .conftest import Session


class UserFactory(alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake user element.
    """

    class Meta:
        model = User
        sqlalchemy_session = Session

    id = LazyAttribute(lambda n: uuid4())
    username = Faker("user_name")
    email = Faker("email")
    password = Faker("password")
