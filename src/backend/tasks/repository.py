from database import new_session


class TaskRepository:
    @classmethod
    async def add_one():
        async with new_session() as session:
            ...

    @classmethod
    async def find_all(): ...
