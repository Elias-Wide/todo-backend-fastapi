from datetime import datetime

from backend.core.constants.ai_services import AiAction
from backend.core.exceptions import AiResponseError
from backend.db.db_manager import DBManager
from backend.schemas.ai_requests import (
    SCreateTaskParams,
    SCreateTaskResponse,
    SErrorResponse,
    SGetNextTaskResponse,
    SGetTasksParams,
    SGetTasksResponse,
)
from backend.services.base import BaseService
from backend.services.tasks import TasksService


class AiService(BaseService):
    """
    Service for orchestrating backend actions based on AI-generated responses.

    This service acts as a bridge between the AI's structured output and the 
    application logic. It parses the validated AI response, maps the 
    identified 'action' to a specific backend method (e.g., task creation, 
    retrieval), and handles error states or unclear user intents.

    Attributes:
        db (DBManager): The database manager for executing task-related queries.
        _action_map (dict): Internal mapping of AiAction enums to service methods.
    """
    def __init__(self, db: DBManager):
        self.tasks_service = TasksService(db)
        self._action_map = {
            AiAction.CREATE_TASKS: self.create_tasks,
            AiAction.GET_TASKS_BY_DATE: self.get_tasks_by_date,
            AiAction.GET_NEXT_TASK: self.get_next_task,
        }

    async def process_request(
        self,
        user_id: int,
        ai_obj: SErrorResponse
        | SCreateTaskResponse
        | SGetTasksResponse
        | SGetNextTaskResponse,
    ):
        """Execute logic based on validated AI response object."""
        action_data = ai_obj
        message = action_data.message
        if action_data.action == AiAction.ERROR:
            raise AiResponseError(action_data.message)

        method = self._action_map.get(action_data.action)
        if not method:
            raise AiResponseError(message)
        params = getattr(action_data, 'parameters', None)
        proccess_action = await method(user_id, params)
        if (
            action_data.action
            in (AiAction.GET_NEXT_TASK, AiAction.GET_TASKS_BY_DATE)
            and proccess_action
        ):
            return {'message': message}
        return {'message': message, 'tasks': proccess_action}

    async def create_tasks(self, user_id: int, params: SCreateTaskParams):
        """Validate and create multiple tasks, returns list of STask."""
        return self.tasks_service.bulk_create_tasks(user_id, params.tasks)

    async def get_tasks_by_date(self, user_id: int, params: SGetTasksParams):
        """Fetch tasks by date string from AI."""
        target_date = datetime.strptime(params.date, '%Y-%m-%d').date()
        return await self.tasks_service.get_task(user_id, target_date)

    async def get_next_task(self, user_id: int, params=None):
        """Fetch the single closest task."""
        return await self.tasks_service.get_next_task(user_id)
