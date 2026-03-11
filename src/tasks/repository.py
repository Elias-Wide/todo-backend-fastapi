from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repository import SQLAlchemyRepository
from src.tasks.models import TasksOrm
from src.tasks.schemas import STask, STaskAdd


class TasksRepository(SQLAlchemyRepository):
    """
    Repository for managing Task entity database operations.
    """

    model: TasksOrm = TasksOrm

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self) -> list[STask]:
        """
        Retrieves all task records from the database.

        Returns:
            List of STask objects representing all tasks in the system.
        """
        model_objs = await super().find_all()
        return [STask.model_validate(obj) for obj in model_objs]

    async def create_task(self, user_id: int, task_data: STaskAdd) -> int:
        """
        Creates a new task record in the database.

        Args:
            user_id: The ID of the user to whom the task belongs.
            task_data: An STaskAdd object containing the task details.

        Returns:
            The ID of the newly created task record.
        """
        task_dict = task_data.model_dump()
        task_dict['user_id'] = user_id
        task = await self.add_one_from_dict(task_dict)
        return STask.model_validate(task)

    async def get_task_by_id(self, user_id: int, task_id: int) -> TasksOrm:
        """
        Retrieves a single task by its ID and user ID.

        Args:
            user_id: The ID of the user to whom the task belongs.
            task_id: The ID of the task to retrieve.
        """
        query = select(self.model).where(
            self.model.id == task_id, self.model.user_id == user_id
        )
        result = await self.session.execute(query)
        task_obj = result.scalar_one_or_none()
        if not task_obj:
            raise ValueError(
                f'Task with ID {task_id} not found for user {user_id}'
            )
        return STask.model_validate(task_obj)

    async def get_tasks_by_user(self, user_id: int) -> list[STask]:
        """
        Retrieves all tasks associated with a specific user.

        Args:
            user_id: The ID of the user whose tasks to retrieve.

        Returns:
            A list of STask objects representing the user's tasks.
        """
        query = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return [STask.model_validate(obj) for obj in result.scalars().all()]
