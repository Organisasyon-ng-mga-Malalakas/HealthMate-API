import pytest
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
    print("test_print", db_user)

    assert str(db_user.id) == user.id
    assert db_user.email == user.email
    assert db_user.username == user.username


def test_get_users(dbsession):
    """Test the `get_users` function."""
    u1 = UserFactory.create()
    u2 = UserFactory.create()

    users = get_users(dbsession)

    for user in users:
        assert str(user.id) in map(lambda x: x.id, [u1, u2])
        assert user.email in map(lambda x: x.email, [u1, u2])
        assert user.username in map(lambda x: x.username, [u1, u2])


def test_create_user(dbsession):
    """Test the `create_user` function."""
    user_data = UserFactory.build()
    user = create_user(dbsession, user_data)

    assert str(user.id) == user_data.id
    assert user.email == user_data.email
    assert user.username == user_data.username
    assert pwd_context.verify(user_data.password, user.password)


# def test_update_user(dbsession, user_factory):
#     """Test the `update_user` function."""
#     user = user_factory.create()

#     user_update_data = {
#         "username": "new_username",
#         "email": "new_email@email.com",
#     }
#     update_user(dbsession, user, user_update_data)

#     assert user.username == user_update_data["username"]
#     assert user.email == user_update_data["email"]


# def test_delete_user(dbsession, user_factory):
#     """Test the `delete_user` function."""
#     user = user_factory.create()

#     delete_user(dbsession, user)

#     assert user.deleted_at is not None
