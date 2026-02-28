from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import SessionLocal, get_session
from backend.db.db_manager import DBManager
from backend.users.models import UsersOrm

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_db_manager() -> AsyncGenerator[DBManager, None]:
    async with DBManager(SessionLocal) as manager:
        yield manager


DBManagerDep = Annotated[DBManager, Depends(get_db_manager)]


async def get_current_user(): ...


UserDep = Annotated[UsersOrm, Depends(get_current_user)]
