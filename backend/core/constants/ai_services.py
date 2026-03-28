from enum import StrEnum


class AiAction(StrEnum):
    """Available actions for the AI assistant to perform."""

    CREATE_TASKS = 'create_tasks'
    GET_TASKS_BY_DATE = 'get_tasks_by_date'
    GET_NEXT_TASK = 'get_next_task'
    ERROR = 'error'


GROQ_TEXT_PROMPT_KEY: str = 'GROQ_PROMPT_SYSTEM'
