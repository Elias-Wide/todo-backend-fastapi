from backend.db.repository import SQLAlchemyRepository
from backend.tasks.models import TasksOrm
from backend.tasks.schemas import STask


class TaskRepository(SQLAlchemyRepository):
    """
    Repository for managing Task entity database operations.
    """

    model = TasksOrm

    @classmethod
    async def find_all(cls) -> list[STask]:
        """
        Retrieves all task records from the database.

        Returns:
            List of STask objects representing all tasks in the system.
        """
        model_objs = await super().find_all()
        return [STask.model_validate(obj) for obj in model_objs]
