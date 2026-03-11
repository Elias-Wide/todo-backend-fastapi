import asyncio
from typing import AsyncGenerator

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.dependecies import get_db_manager
from db.db_manager import DBManager
from main import app

TEST_DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def db_session() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=TestSessionLocal) as manager:
        yield manager


def run_migrations(connection):
    config = Config('alembic.ini')
    config.set_main_option('sqlalchemy.url', TEST_DATABASE_URL)
    command.upgrade(config, 'head')


def downgrade_migrations(connection):
    config = Config('alembic.ini')
    config.set_main_option('sqlalchemy.url', TEST_DATABASE_URL)
    command.downgrade(config, 'base')


@pytest.fixture(scope='function')
async def db_session():
    # Прогоняем миграции вверх
    async with test_engine.begin() as conn:
        await conn.run_sync(run_migrations)

    async with DBManager(session_factory=TestSessionLocal) as manager:
        yield manager

    # Откатываем миграции вниз (чтобы база была чистой)
    async with test_engine.begin() as conn:
        await conn.run_sync(downgrade_migrations)


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
