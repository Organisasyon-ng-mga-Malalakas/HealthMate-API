from app.api.symptoms.symptoms_service import SymptomsService
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_symptoms(birth_year: int, gender: str, body_part: str):
    symptoms = SymptomsService(
        birth_year=birth_year, gender=gender, body_part=body_part
    )
    return symptoms.get_symptoms()
