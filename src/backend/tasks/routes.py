from typing import Annotated

from fastapi import APIRouter, Depends

from backend.tasks.dependecies import get_task_service
from backend.tasks.repository import TaskRepository
from backend.tasks.schemas import STask, STaskAdd
from backend.tasks.services import TasksService

router = APIRouter(prefix='/tasks', tags=['Tasks'])


@router.get('')
async def get_tasks(
    task_service: TasksService = Annotated[
        TasksService, Depends(get_task_service)
    ],
) -> list[STask]:
    return await TaskRepository.find_all()


@router.post('')
async def add_task(
    task: Annotated[STaskAdd, Depends()],
    task_service: Annotated[TasksService, Depends(get_task_service)],
):
    task_id = await task_service.create_task(task)
    return {'id': task_id}
