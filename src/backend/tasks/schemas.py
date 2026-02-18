from typing import Optional

from pydantic import BaseModel, Field


class STaskAdd(BaseModel):
    """
    Schema for creating a new task.

    Contains the core information required to initialize a task
    within the system.
    """

    title: str = Field(..., description='The brief title of the task')
    category: str = Field(
        ..., description='The logical grouping or tag for the task'
    )
    description: Optional[str] = Field(
        None, description="Detailed explanation of the task's scope"
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
