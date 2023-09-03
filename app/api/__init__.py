from fastapi import APIRouter
from app.api.user.routes import router as user_router
from app.api.symptoms.routes import router as symptoms_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(symptoms_router, prefix="/symptoms", tags=["Symptoms"])
