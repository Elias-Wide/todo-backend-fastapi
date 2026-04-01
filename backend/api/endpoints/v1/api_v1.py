from fastapi import APIRouter

from api.endpoints.v1.tasks import router as tasks_router
from api.endpoints.v1.users import router as users_router

api_v1_router = APIRouter(prefix='/v1')

api_v1_router.include_router(users_router)
api_v1_router.include_router(tasks_router)
