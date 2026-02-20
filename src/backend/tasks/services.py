from backend.tasks.models import TasksOrm
from backend.tasks.repository import TaskRepository
from backend.tasks.schemas import STask


class TasksService:
    """Service layer for Task entities and business logic."""

    def __init__(self, repository: TaskRepository):
        """Initialize the service with a task repository."""
        self.repo: TaskRepository = repository

    async def create_task(self, task_data: STask) -> int:
        """
        Create a new task and return its unique ID.

        Returns:
            The ID of the newly created task record.
        """
        return await self.repo.add_one(task_data)

    async def get_task(self, task_id: int) -> TasksOrm:
        """
        Retrieve a single task by its ID.

        Raises:
            ValueError: If the task does not exist.
        """
        return await self.repo.get_one(record_id=task_id)

    async def update_task(self, task_id: int, task_data: STask) -> TasksOrm:
        """
        Update an existing task with the provided data.

        Returns:
            The updated TasksOrm instance.
        """
        task = await self.get_task(task_id)
        return await self.repo.update(db_obj=task, obj_in=task_data)

    async def delete_task(self, task_id: int) -> None:
        """
        Delete a task from the database by its ID.

        Raises:
            ValueError: If the task is not found.
        """
        task = await self.get_task(task_id)
        await self.repo.delete(db_obj=task)
