from fastapi import APIRouter
from app.api.user.routes import router as user_router
from app.api.symptoms.routes import router as symptoms_router
from app.api.questions.routes import router as questions_router
from app.api.schedule.routes import router as schedule_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(symptoms_router, prefix="/symptoms", tags=["Symptoms"])
api_router.include_router(questions_router, prefix="/questions", tags=["Questions"])
api_router.include_router(schedule_router, prefix="/schedule", tags=["Schedule"])
