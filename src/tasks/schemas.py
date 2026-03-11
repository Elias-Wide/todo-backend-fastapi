from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.tasks.constants import (
    DESCRIPTION_MAX_LENGTH,
    TASK_MAX_LENGTH,
    TASK_MIN_LENGTH,
)


class STaskAdd(BaseModel):
    """
    Schema for creating a new task.

    Contains the core information required to initialize a task
    within the system.
    """

    title: str = Field(
        ..., min_length=TASK_MIN_LENGTH, max_length=TASK_MAX_LENGTH
    )
    description: Optional[str] = Field(None, max_length=DESCRIPTION_MAX_LENGTH)
    is_daily: bool = Field(
        False, description='Indicates if the task should repeat daily'
    )
    model_config = ConfigDict(from_attributes=True)
    scheduled_time: Optional[datetime] = Field(
        None,
        examples=[
            '2023-10-27T10:00:00',
        ],
        description='Specific time of day the task, in HH:MM format',
        json_schema_extra={'format': 'date-time'},
    )


class STask(STaskAdd):
    """
    Complete task representation.

    Extends STaskAdd by including system-generated fields
    such as the unique identifier.
    Used for data retrieval and response serialization.
    """

    id: int = Field(
        ..., description='The unique database identifier for the task'
    )
    model_config = ConfigDict(from_attributes=True)
