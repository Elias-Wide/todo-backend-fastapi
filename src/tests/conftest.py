import asyncio
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.api.dependecies import get_db_manager
from src.core.constants import MAIN_API_ROUTE
from src.db.database import Model
from src.db.db_manager import DBManager
from src.main import app
from src.tests.fixtures.users import *  # noqa: F403, F401

TEST_DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture
def main_api_route() -> str:
    return MAIN_API_ROUTE


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def db_session() -> AsyncGenerator[DBManager, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    async with DBManager(session_factory=TestSessionLocal) as manager:
        yield manager
    async with test_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


@pytest.fixture(scope='function')
async def client(db_session: DBManager) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db_manager():
        yield db_session

    app.dependency_overrides[get_db_manager] = override_get_db_manager
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
