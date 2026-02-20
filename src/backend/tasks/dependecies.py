from backend.tasks.services import TasksService
from backend.users.repository import TaskRepository


def get_task_service() -> TasksService:
    """Dependency function to provide a TasksService instance."""
    return TasksService(repository=TaskRepository())
