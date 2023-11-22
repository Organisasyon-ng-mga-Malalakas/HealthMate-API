from app.api.symptoms.symptoms_service import SymptomsService
from fastapi import APIRouter, Body
from typing import Literal

router = APIRouter()


@router.get("/")
async def get_symptoms(
    birth_year: int,
    gender: Literal["male", "female"],
    body_part: Literal[
        "head", "upperbody", "lowerbody", "legs", "arms", "general"
    ],
):
    symptoms = SymptomsService(
        birth_year=birth_year, gender=gender, body_part=body_part
    )
    return symptoms.get_symptoms()


@router.get("/result")
async def get_diseases_from_symptoms(
    birth_year: int,
    gender: Literal["male", "female"],
    body_part: Literal[
        "head", "upperbody", "lowerbody", "legs", "arms", "general"
    ],
    symptom_ids: str,
):
    symptoms = SymptomsService(
        birth_year=birth_year, gender=gender, body_part=body_part
    )
    return symptoms.get_diseases_from_symptoms(symptom_ids.split(","))


@router.get("/details/{diagnosis_id}")
async def get_condition_details(
    birth_year: int,
    gender: Literal["male", "female"],
    body_part: Literal[
        "head", "upperbody", "lowerbody", "legs", "arms", "general"
    ],
    diagnosis_id: int,
):
    symptoms = SymptomsService(
        birth_year=birth_year, gender=gender, body_part=body_part
    )
    return symptoms.get_condition_details(diagnosis_id)
