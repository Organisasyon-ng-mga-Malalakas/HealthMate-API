from datetime import datetime, timedelta
from typing import List, Optional

import app.api.user.controller as user_controller
from app.api.user.schemas import User, UserCreate, UserUpdate
from app.core.config import settings
from app.core.schemas import Token
from app.database import get_db
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=User)
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_controller.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Account already registered")
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


@router.put("/users/{username}", response_model=User)
async def update_user_route(
    username: str, user: UserUpdate, db: Session = Depends(get_db)
):
    db_user = user_controller.get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_controller.update_user(db, db_user, user)


@router.delete("/users/{username}", response_model=User)
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
