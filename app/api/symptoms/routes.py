from datetime import datetime, timedelta
from typing import List, Optional

import app.api.user.controller as user_controller
import app.api.symptoms.controller as symptoms_controller
from app.api.symptoms.symptoms_service import SymptomsService
from app.api.user.schemas import User, UserCreate, UserUpdate
from app.core.config import settings
from app.core.schemas import Token
from app.database import get_db
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def get_symptoms(birth_year: int, gender: str, body_part: str):
    symptoms = SymptomsService(
        birth_year=birth_year, gender=gender, body_part=body_part
    )
    return symptoms.get_symptoms()
