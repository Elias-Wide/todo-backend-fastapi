from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, RootModel

from src.core.constants.ai_services import AiAction


class SAiRequest(BaseModel):
    """User request sent to the AI assistant."""

    text: str = Field(..., description="The user's message text")


class STaskData(BaseModel):
    """Detailed fields for creating a new task."""

    title: str = Field(..., description='Task title')
    description: Optional[str] = Field(None, description='Task details')
    scheduled_time: Optional[str] = Field(
        None, description='Format: YYYY-MM-DD HH:MM'
    )
    date: str = Field(..., description='Task date: YYYY-MM-DD')


class SCreateTaskParams(BaseModel):
    """Parameters for the create_task action."""

    tasks: STaskData = Field(..., description='The task data object')
    message: str = Field(..., description='Confirmation for the user')


class SErrorParams(BaseModel):
    """Parameters for an execution error."""

    message: str = Field(..., description='Error message for the user')


class SGetTasksParams(BaseModel):
    """Parameters for retrieving tasks by date."""

    date: str = Field(..., description='Target date: YYYY-MM-DD')


class SErrorResponse(BaseModel):
    """Response returned when an error occurs."""

    action: Literal[AiAction.ERROR]
    parameters: SErrorParams


class SCreateTaskResponse(BaseModel):
    """Response returned to trigger task creation."""

    action: Literal[AiAction.CREATE_TASKS]
    parameters: SCreateTaskParams


class SGetTasksResponse(BaseModel):
    """Response returned to fetch tasks for a date."""

    action: Literal[AiAction.GET_TASKS_BY_DATE]
    parameters: SGetTasksParams


class SGetNextTaskResponse(BaseModel):
    """Response for the 'nearest' or 'upcoming' task."""

    action: Literal[AiAction.GET_NEXT_TASK]


class SAiResponse(RootModel):
    """Unified AI response model with discriminator 'action'."""

    root: Union[
        SErrorResponse,
        SCreateTaskResponse,
        SGetTasksResponse,
        SGetNextTaskResponse,
    ] = Field(..., discriminator='action')
