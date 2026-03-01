class DbLogMessages:
    """Messages for internal database operation logging."""

    COMMIT_SUCCESS = 'Record successfully saved to DB. ID: %s'
    INTEGRITY_ERROR = 'Data integrity error saving %s: %s'
    DB_OP_ERROR = "SQLAlchemy error in method '%s': %s"
    FETCH_ERROR = 'Database error while fetching records: %s'
    UNEXPECTED_ERROR = "Unexpected system error in method '%s': %s"
    NOT_FOUND = 'No %s record found with ID: %s'


class DbErrorMessages:
    """Error messages for database-related exceptions."""

    ALREADY_EXISTS = 'The object {model} with data {data} already exists.'
    SAVE_FAILED = 'Failed to save the record to the database.'
    FETCH_FAILED = 'Failed to retrieve the list of objects.'
    INTERNAL_ERROR = 'Internal server error occurred during DB operation.'
    NOT_FOUND = 'No {model} found with ID {id}.'
