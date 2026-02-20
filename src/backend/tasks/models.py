from datetime import datetime, time
from typing import Optional

from sqlalchemy import Time, func, text
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.database import Model


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
    is_daily: Mapped[bool] = mapped_column(
        server_default=text('false'),
        default=False,
        comment='Indicates if the task should repeat every 24 hours',
    )
    scheduled_time: Mapped[Optional[time]] = mapped_column(
        Time,
        nullable=True,
        comment='Specific time of day the task is set to occur',
    )
    expired_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
        comment='The final deadline timestamp for task completion',
    )

    def __repr__(self) -> str:
        """
        Returns a developer-friendly string representation of the task.
        """
        return f'<TasksOrm(title={self.title}, is_daily={self.is_daily})>'

    def __str__(self):
        return f'{self.title}'
