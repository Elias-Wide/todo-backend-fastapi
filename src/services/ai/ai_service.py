from datetime import datetime

from src.core.constants.ai_services import AiAction
from src.core.exceptions import AiResponseError
from src.db.db_manager import DBManager
from src.schemas.ai_requests import (
    SAiResponse,
    SCreateTaskParams,
    SGetTasksParams,
)
from src.schemas.tasks import STaskAdd
from src.services.base import BaseService


class AiService(BaseService):
    def __init__(self, db: DBManager):
        self.db = db
        self._action_map = {
            AiAction.CREATE_TASKS: self.create_tasks,
            AiAction.GET_TASKS_BY_DATE: self.get_tasks_by_date,
            AiAction.GET_NEXT_TASK: self.get_next_task,
        }

    async def process_request(self, user_id: int, ai_obj: SAiResponse):
        """Execute logic based on validated AI response object."""
        action_data = ai_obj.root
        message = action_data.parameters.message
        if action_data.action == AiAction.ERROR:
            raise AiResponseError(action_data.parameters.message)

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
        created_tasks = []
        for t in params.tasks:
            task_to_add = STaskAdd(t)
            task_obj = await self.db.tasks.create_task(user_id, task_to_add)
            created_tasks.append(task_obj)
        return created_tasks

    async def get_tasks_by_date(self, user_id: int, params: SGetTasksParams):
        """Fetch tasks by date string from AI."""
        target_date = datetime.strptime(params.date, '%Y-%m-%d').date()
        return await self.db.tasks.get_tasks_by_date(user_id, target_date)

    async def get_next_task(self, user_id: int, params=None):
        """Fetch the single closest task."""
        return await self.db.tasks.get_next_task(user_id)
