from datetime import date

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.tasks import TasksOrm
from backend.repositories.base import SQLAlchemyRepository
from backend.schemas.tasks import STask, STaskAdd


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

    async def get_tasks_by_date(
        self, user_id: int, target_date: date
    ) -> list[STask]:
        """
        Retrieves all tasks for a specific user and date.
        """
        query = select(self.model).where(
            self.model.user_id == user_id,
            func.date(self.model.created_at) == target_date,
        )
        result = await self.session.execute(query)
        return [STask.model_validate(obj) for obj in result.scalars().all()]

    async def get_next_task(self, user_id: int) -> STask | None:
        """
        Retrieves the closest upcoming task for a specific user.
        """
        query = (
            select(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.scheduled_time >= func.now(),
            )
            .order_by(self.model.scheduled_time.asc())
            .limit(1)
        )
        result = await self.session.execute(query)
        task_obj = result.scalar_one_or_none()

        if not task_obj:
            return None

        return STask.model_validate(task_obj)

    async def bulk_create_tasks(
        self, user_id: int, tasks_data: list[STaskAdd]
    ) -> list[TasksOrm]:
        """Bulk create tasks and return the list of created ORM instances."""
        if not tasks_data:
            return []
        values = [
            {**task.model_dump(), "user_id": user_id} 
            for task in tasks_data
        ]
        stmt = insert(self.model).values(values).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return list(result.scalars().all())