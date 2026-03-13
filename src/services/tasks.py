from src.core.exceptions import AccessDeniedError, TaskNotFoundError
from src.db.db_manager import DBManager
from src.models.tasks import TasksOrm
from src.tasks.schemas import STask


class TasksService:
    """Service layer for Task entities and business logic."""

    def __init__(self, db: DBManager):
        """Initialize the service with a task repository."""
        self.db: DBManager = db

    async def create_task(self, user_id: int, task_data: STask) -> int:
        """
        Create a new task and return its unique ID.

        Returns:
            The ID of the newly created task record.
        """
        return await self.db.tasks.create_task(
            user_id=user_id, task_data=task_data
        )

    async def get_task(self, user_id: int, task_id: int) -> TasksOrm:
        """
        Retrieve a single task by its ID.

        Raises:
            ValueError: If the task does not exist.
        """
        try:
            return await self.db.tasks.get_task_by_id(
                user_id=user_id, task_id=task_id
            )
        except ValueError as e:
            raise TaskNotFoundError from e

    async def update_task(
        self, user_id: int, task_id: int, task_data: STask
    ) -> TasksOrm:
        """
        Update an existing task with the provided data.

        Returns:
            The updated TasksOrm instance.
        """
        task = await self.get_task(user_id, task_id)
        return await self.db.tasks.update(db_obj=task, obj_in=task_data)

    async def delete_task(self, user_id: int, task_id: int) -> None:
        """
        Delete a task from the database by its ID.

        Raises:
            ValueError: If the task is not found.
        """
        task: TasksOrm = await self.db.tasks.get_one_by_field('id', task_id)
        if not task:
            raise TaskNotFoundError(f'Task {task_id} not found')
        if task.user_id != user_id:
            raise AccessDeniedError()
        await self.db.tasks.delete(db_obj=task)
        await self.db.commit()

    async def get_user_tasks(self, user_id: int) -> list[STask]:
        """
        Retrieve all tasks associated with a specific user.

        Returns:
            A list of STask instances representing the user's tasks.
        """
        return await self.db.tasks.get_tasks_by_user(user_id=user_id)
