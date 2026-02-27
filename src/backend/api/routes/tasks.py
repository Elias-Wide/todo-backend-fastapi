from typing import Annotated

from backend.api.dependecies import DBManagerDep
from backend.tasks.schemas import STask, STaskAdd
from backend.tasks.services import TasksService
from backend.users.models import UsersOrm
from fastapi import APIRouter, Depends

router = APIRouter(prefix='/tasks', tags=['Tasks'])


@router.get('')
async def get_tasks(
    user: Annotated[UsersOrm, Depends(get_current_user)],
    db: DBManagerDep,
) -> list[STask]:
    service = TasksService(db)
    return await service.get_tasks_for_user(user=user)


@router.post('')
async def add_task(
    user: Annotated[UsersOrm, Depends(get_current_user)],
    task: Annotated[STaskAdd, Depends()],
    db: DBManagerDep,
):
    service = TasksService(db)
    task_id = await service.create_task(user, task)
    return {'id': task_id}
