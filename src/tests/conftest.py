import os
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from src.dependencies.db_manager import get_db_manager
from src.dependencies.users import get_current_user

os.environ['APP_MODE'] = 'TEST'

from src.core.constants.core import MAIN_API_ROUTE
from src.db.database import Model, SessionLocal, engine
from src.db.db_manager import DBManager
from src.main import app
from src.tests.fixtures.tasks import *
from src.tests.fixtures.users import *


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    """Create tables once for the whole test session."""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope='function')
async def db_session() -> AsyncGenerator[DBManager, None]:
    """Provides a DBManager and cleans data after each test via rollback."""
    async with DBManager(session_factory=SessionLocal) as manager:
        yield manager
    async with engine.begin() as conn:
        for table in reversed(Model.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest.fixture(scope='function')
async def client(db_session: DBManager) -> AsyncGenerator[AsyncClient, None]:
    """Client that uses the shared db_session from the fixture."""

    async def override_get_db_manager():
        yield db_session

    app.dependency_overrides[get_db_manager] = override_get_db_manager

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(scope='function')
async def client_with_user(
    client: AsyncClient, db_session: DBManager, registered_user
) -> AsyncGenerator[AsyncClient, None]:
    """
    Extends the base client by mocking the current user.
    """

    async def override_current_user():
        return registered_user

    app.dependency_overrides[get_current_user] = override_current_user
    yield client
    del app.dependency_overrides[get_current_user]


@pytest.fixture
def main_api_route() -> str:
    return MAIN_API_ROUTE
