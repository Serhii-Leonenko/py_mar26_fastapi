from fastapi import APIRouter

from api.v1.users import router as users_router
from api.v1.projects import router as projects_router
from api.v1.task import router as tasks_router
from api.v1.auth import router as auth_router


api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(projects_router)
api_router.include_router(tasks_router)
api_router.include_router(auth_router)
