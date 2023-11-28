from datetime import datetime, timedelta
from typing import List, Optional

import app.models as models
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.api.user.controller as user_controller
from app.api.user.schemas import User, UserCreate, UserUpdate
from app.core.config import settings
from app.core.mail_service import (
    send_forgot_password_email,
    send_new_password_email,
)
from app.core.schemas import Token
from app.core.security import pwd_context
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=User)
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_controller.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Account already registered"
        )
    return user_controller.create_user(db, user)


@router.get("/", response_model=List[User])
async def read_users(db: Session = Depends(get_db)):
    return user_controller.get_users(db)


@router.get("/{username}", response_model=User)
async def read_user(username: str, db: Session = Depends(get_db)):
    db_user = user_controller.get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{username}", response_model=User)
async def update_user_route(
    username: str, user: UserUpdate, db: Session = Depends(get_db)
):
    db_user = user_controller.get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_controller.update_user(db, db_user, user)


@router.delete("/{username}", response_model=User)
async def delete_user_route(username: str, db: Session = Depends(get_db)):
    db_user = user_controller.get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_controller.delete_user(db, db_user)


@router.post("/login", response_model=Token)
async def login_access_token_route(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_controller.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    access_token_expires = timedelta(
        minutes=settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = user_controller.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/forgot-password/confirm/{hash}")
async def generate_new_password(hash: str, db: Session = Depends(get_db)):
    fp_data = user_controller.check_forgot_password_identifier(db, hash)
    if not fp_data:
        raise HTTPException(status_code=404, detail="Invalid request")

    # DELETE USER RECORDS IN FW TABLE
    db.query(models.ForgotPassword).filter(
        models.ForgotPassword.user_id == fp_data.user_id
    ).delete()

    # UPDATE USER PASSWORD
    new_pass = user_controller.generate_random_identifier()
    hashed_password = pwd_context.hash(new_pass)

    user = (
        db.query(models.User).filter(models.User.id == fp_data.user_id).first()
    )

    user.password = hashed_password

    db.commit()

    if not send_new_password_email(user.username, new_pass):
        {"new_pass": new_pass}

    return {
        "status": "success",
        "message": "We have sent your new password at your email!",
    }


@router.get("/forgot-password/{username}")
async def forgot_password(username: str, db: Session = Depends(get_db)):
    db_user = user_controller.get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_controller.check_forgot_password_data(db, db_user.id):
        raise HTTPException(
            status_code=400,
            detail="You already have a new forgot password request.",
        )

    forgot_pass_identifier = user_controller.create_forgot_password_data(
        db, db_user.id
    )

    if not forgot_pass_identifier:
        raise HTTPException(
            status_code=400,
            detail="Unable to process forgot password. Please check your email for existing forgot password requests.",
        )

    if not send_forgot_password_email(db_user.username, forgot_pass_identifier):
        raise HTTPException(
            status_code=400,
            detail="Unable to process forgot password right now.",
        )

    return {"status": "success"}
