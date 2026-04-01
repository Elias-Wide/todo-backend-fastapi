import json
import re
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from config import settings
from core.exceptions import AiResponseError, TaskNotFoundError
from dependencies.db_manager import DBManagerDep
from dependencies.users import get_current_user
from models.users import UsersOrm
from schemas.ai_requests import SAiRequest, SAiResponse
from schemas.tasks import STask, STaskAdd
from services.ai.ai_service import AiService
from services.ai.clients import GroqTextClient
from services.ai.utils import prompt_text
from services.tasks import TasksService

router = APIRouter(prefix='/tasks', tags=['Tasks'])


@router.get('')
async def get_tasks(
    user: Annotated[UsersOrm, Depends(get_current_user)],
    db: DBManagerDep,
) -> list[STask]:
    service = TasksService(db)
    return await service.get_user_tasks(user_id=user.id)


@router.post('')
async def add_task(
    user: Annotated[UsersOrm, Depends(get_current_user)],
    task: Annotated[STaskAdd, Depends()],
    db: DBManagerDep,
):
    service = TasksService(db)
    task_id = await service.create_task(user.id, task)
    return {'id': task_id}


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user: Annotated[UsersOrm, Depends(get_current_user)],
    task_id: int,
    db: DBManagerDep,
):
    service = TasksService(db)
    try:
        await service.delete_task(user_id=user.id, task_id=task_id)
        return
    except TaskNotFoundError as err:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=str(err)
        ) from err


@router.post('/send_ai_request')
async def send_ai_request(
    user: Annotated[UsersOrm, Depends(get_current_user)],
    text: Annotated[SAiRequest, Depends()],
    db: DBManagerDep,
):
    current_dt = datetime.now()
    formatted_prompt = prompt_text % (
        current_dt.strftime('%Y-%m-%d %H:%M'),
        user.lang,
    )
    llm = GroqTextClient(
        settings.ai.api_key,
        model=settings.ai.text_model,
        system_prompt=formatted_prompt,
    )
    raw_answer: str = llm.send_request(text)
    match = re.search(r'(\{.*\})', raw_answer, re.DOTALL)
    if match:
        try:
            print(json.loads(raw_answer))
            ai_response = SAiResponse.model_validate_json(match.group(1)).root
            print(ai_response)
            ai_service = AiService(db)
            return await ai_service.process_request(user.id, ai_response)
        except ValidationError as e:
            return {'error': 'Invalid AI structure', 'details': e.errors()}
        except AiResponseError as e:
            return {'error': str(e.msg)}
    return {'error': 'Could not parse AI response', 'raw': raw_answer}
