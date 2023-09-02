import pytest
from app.api.user.schemas import UserUpdate
from app.api.user.controller import (
    create_user,
    delete_user,
    get_user,
    get_users,
    update_user,
)

from app.core.security import pwd_context
from tests.factory import UserFactory


def test_get_user(dbsession):
    """Test the `get_user` function."""
    user = UserFactory.create()

    db_user = get_user(dbsession, user.username)

    for k in db_user.__dict__.keys():
        if not k.startswith("_"):
            assert hasattr(user, k)
            assert getattr(db_user, k) == getattr(user, k, None)


def test_get_users(dbsession):
    """Test the `get_users` function."""
    u1 = UserFactory.create()
    u2 = UserFactory.create()

    users = get_users(dbsession)

    assert len(users) == 2

    for user in users:
        assert user.id in map(lambda x: x.id, [u1, u2])
        assert user.email in map(lambda x: x.email, [u1, u2])
        assert user.username in map(lambda x: x.username, [u1, u2])


def test_create_user(dbsession):
    """Test the `create_user` function."""
    user_data = UserFactory.build()
    user = create_user(dbsession, user_data)

    assert pwd_context.verify(user_data.password, user.password)

    _exceptions = (
        "password",
        "created_at",
    )
    for k in user.__dict__.keys():
        if not k.startswith("_") and k not in _exceptions:
            assert getattr(user, k) == getattr(user_data, k, None)


def test_update_user(dbsession):
    """Test the `update_user` function."""
    user = UserFactory.create()

    db_user = get_user(dbsession, user.username)

    user_update_data = {
        "username": "new_username",
        "email": "new_email@email.com",
    }
    updated_user = update_user(
        dbsession, db_user, UserUpdate(**user_update_data)
    )

    assert updated_user.username == user_update_data["username"]
    assert updated_user.email == user_update_data["email"]


def test_delete_user(dbsession):
    """Test the `delete_user` function."""
    user = UserFactory.create()

    delete_user(dbsession, user)

    assert user.deleted_at is not None
