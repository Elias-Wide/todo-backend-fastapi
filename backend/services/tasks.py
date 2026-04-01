from datetime import datetime

from core.exceptions import AccessDeniedError, TaskNotFoundError
from models.tasks import TasksOrm
from schemas.tasks import STask, STaskAdd
from services.base import BaseService


class TasksService(BaseService):
    """Service layer for Task entities and business logic."""

    async def create_task(self, user_id: int, task_data: STask) -> int:
        """Create a new task and return its unique ID."""
        task = await self.db.tasks.create_task(
            user_id=user_id, task_data=task_data
        )
        await self.db.session.commit()
        return task

    async def get_task(self, user_id: int, task_id: int) -> TasksOrm:
        """Retrieve a single task by its ID or raise TaskNotFoundError."""
        try:
            return await self.db.tasks.get_task_by_id(
                user_id=user_id, task_id=task_id
            )
        except ValueError as e:
            raise TaskNotFoundError from e

    async def update_task(
        self, user_id: int, task_id: int, task_data: STask
    ) -> TasksOrm:
        """Update an existing task and return the updated ORM instance."""
        task = await self.get_task(user_id, task_id)
        return await self.db.tasks.update(db_obj=task, obj_in=task_data)

    async def delete_task(self, user_id: int, task_id: int) -> None:
        """Delete a task by ID or raise Error if not found or unauthorized."""
        task: TasksOrm = await self.db.tasks.get_one_by_field('id', task_id)
        if not task:
            raise TaskNotFoundError(f'Task {task_id} not found')
        if task.user_id != user_id:
            raise AccessDeniedError()
        await self.db.tasks.delete(db_obj=task)
        await self.db.commit()

    async def get_user_tasks(self, user_id: int) -> list[STask]:
        """Retrieve all tasks associated with a specific user."""
        return await self.db.tasks.get_tasks_by_user(user_id=user_id)

    async def bulk_create_tasks(
        self, user_id: int, tasks_data: list[STaskAdd]
    ) -> list[TasksOrm]:
        """Validate and bulk create tasks within a single transaction."""
        if not tasks_data:
            raise ValueError('Task list cannot be empty')
        try:
            tasks = await self.db.tasks.bulk_create_tasks(user_id, tasks_data)
            await self.db.commit()
            return tasks
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_tasks_by_date(
        self, user_id: int, target_date: datetime
    ) -> list[STask]:
        """Retrieve all tasks for a specific date for the given user."""
        return await self.db.tasks.get_tasks_by_date(user_id, target_date)

    async def get_next_task(self, user_id: int) -> STask | None:
        """Get the next scheduled task for the user, validated as STask."""
        task_obj = await self.db.tasks.get_next_task(user_id)
        if not task_obj:
            return None
        return STask.model_validate(task_obj)
