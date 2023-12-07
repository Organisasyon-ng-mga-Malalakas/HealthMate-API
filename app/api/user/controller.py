import secrets
import string
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from jose import jwt
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.user.schemas import UserCreate, UserUpdate
from app.core.config import settings
from app.core.security import pwd_context
from app.models import ForgotPassword, User


def get_user(db: Session, username: str) -> Optional[User]:
    return (
        db.query(User)
        .filter(User.username == username, User.deleted_at == None)
        .first()
    )


def get_user_by_id(db: Session, id: str) -> Optional[User]:
    if not is_valid_uuid4(id):
        return None
    return db.query(User).filter(User.id == id).first()


def get_users(db: Session) -> List[User]:
    return db.query(User).filter(User.deleted_at == None).all()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        id=user.id or str(uuid.uuid4()),
        username=user.username,
        email=user.email,
        gender=user.gender,
        birthdate=user.birthdate,
        password=hashed_password,
        created_at=datetime.utcnow(),
        deleted_at=None,
        updated_at=None,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User, user_update: UserUpdate) -> User:
    user.username = user_update.username or user.username
    user.email = user_update.email or user.email
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, user: User, password: str) -> User:
    user.password = password
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> User:
    user.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


# Define authentication
def authenticate_user(db: Session, username: str, password):
    user = get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.AUTH_SECRET_KEY,
        algorithm=settings.AUTH_ALGORITHM,
    )
    return encoded_jwt


def create_forgot_password_data(db: Session, userid):
    identifier = generate_random_identifier()
    forgot_pass = ForgotPassword(
        user_id=userid,
        status="pending",
        created_at=datetime.utcnow(),
        identifier=identifier,
    )
    db.add(forgot_pass)
    db.commit()
    return identifier


def check_forgot_password_data(db: Session, userid):
    try:
        forgot_pass = (
            db.query(ForgotPassword)
            .filter(
                ForgotPassword.user_id == userid,
                ForgotPassword.created_at
                <= func.timezone("UTC", func.now()) - timedelta(seconds=60),
            )
            .first()
        )
    except:
        return False
    return forgot_pass


def check_forgot_password_identifier(db: Session, identifier: str = ""):
    try:
        forgot_pass = (
            db.query(ForgotPassword)
            .filter(
                ForgotPassword.identifier == identifier,
            )
            .first()
        )
    except:
        return False
    return forgot_pass


def generate_random_identifier():
    alphabet = string.ascii_letters + string.digits
    identifier = "".join(secrets.choice(alphabet) for _ in range(12))
    return identifier

def is_valid_uuid4(s):
    try:
        uuid_obj = uuid.UUID(s, version=4)
        return str(uuid_obj) == s
    except ValueError:
        return False