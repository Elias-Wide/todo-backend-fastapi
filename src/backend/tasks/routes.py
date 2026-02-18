from typing import Annotated
from fastapi import APIRouter, Depends

from src.backend.tasks.schemas import STaskAdd


router = APIRouter(prefix="/tasks", tags=["Tasks"])

router.get("/")
async def get_tasks():
    ...

router.post("/")
async def add_task(task: Annotated[STaskAdd, Depends]):
    ...