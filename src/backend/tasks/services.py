from backend.db.db_manager import DBManager
from backend.tasks.models import TasksOrm
from backend.tasks.schemas import STask


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
        return await self.db.tasks.get_task_by_id(
            user_id=user_id, task_id=task_id
        )

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
        task = await self.get_task(user_id, task_id)
        await self.db.tasks.delete(db_obj=task)
