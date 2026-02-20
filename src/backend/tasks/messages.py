class TaskErrorMessages:
    """User-facing messages (formatted with .format())"""

    ALREADY_EXISTS = "Task with title '{title}' already exists."
    SAVE_FAILED = 'Failed to save the task. Please try again later.'
    NOT_FOUND = 'Task with ID {task_id} was not found.'
    FETCH_FAILED = 'Could not retrieve tasks from the database.'
    INTERNAL_ERROR = 'A technical error occurred on the server.'
