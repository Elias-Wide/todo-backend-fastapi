from datetime import datetime, time
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Model
from models.users import UsersOrm


def default_task_time():
    return time(10, 0)


class TasksOrm(Model):
    """
    Represents a task within the database schema.

    This model stores core task information, including its recurrence
    status, creation timestamps, and specific execution schedules.
    """

    title: Mapped[str] = mapped_column(
        comment='Primary title or heading of the task'
    )
    description: Mapped[Optional[str]] = mapped_column(
        comment="Detailed explanation of the task's requirements"
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        comment='Timestamp when the record was initially created',
    )
    scheduled_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=default_task_time,
        comment='Specific time of day the task is set to occur',
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='Foreign key linking the task to its owning user',
    )
    user: Mapped[UsersOrm] = relationship(back_populates='tasks')

    def __repr__(self) -> str:
        """
        Returns a developer-friendly string representation of the task.
        """
        return f'<TasksOrm(title={self.title})>'

    def __str__(self):
        return f'{self.title}'
