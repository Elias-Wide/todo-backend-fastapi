from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.core.constants.tasks import (
    DEFAULT_TASK_TIME,
    DESCRIPTION_MAX_LENGTH,
    TASK_MAX_LENGTH,
    TASK_MIN_LENGTH,
)


class STaskAdd(BaseModel):
    """Schema for creating a task with a single scheduled timestamp."""

    title: str = Field(..., min_length=TASK_MIN_LENGTH, max_length=TASK_MAX_LENGTH)
    description: Optional[str] = Field(None, max_length=DESCRIPTION_MAX_LENGTH)    
    scheduled_at: datetime = Field(
        default_factory=lambda: datetime.now().replace(
            hour=DEFAULT_TASK_TIME, minute=0, second=0, microsecond=0
        ),
        description="Task date and time. If time is missing, defaults to 10:00."
    )

    @field_validator("scheduled_at", mode="before")
    @classmethod
    def set_default_time(cls, v):
        if isinstance(v, str):
            if len(v.strip()) == 10:
                dt = datetime.strptime(v, "%Y-%m-%d")
                return dt.replace(hour=10, minute=0)
        return v

    model_config = ConfigDict(from_attributes=True)


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
