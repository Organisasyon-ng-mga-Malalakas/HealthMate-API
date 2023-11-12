from app.api.symptoms.symptoms_service import SymptomsService
from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/")
async def get_symptoms(birth_year: int, gender: str, body_part: str):
    symptoms = SymptomsService(
        birth_year=birth_year, gender=gender, body_part=body_part
    )
    return symptoms.get_symptoms()


@router.post("/result")
async def get_diseases_from_symptoms(
    birth_year: int = Body(...),
    gender: str = Body(...),
    body_part: str = Body(...),
    symptom_ids: list[int] = Body(...),
):
    symptoms = SymptomsService(
        birth_year=birth_year, gender=gender, body_part=body_part
    )
    return symptoms.get_diseases_from_symptoms(symptom_ids)
