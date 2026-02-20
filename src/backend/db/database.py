from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

from backend.core.config import settings

engine = create_async_engine(url=settings.db.url, echo=True)

new_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class PreBase:
    """Base class for all ORM models with common attrs and methods."""

    @declared_attr
    def __tablename__(self) -> str:
        """Returns the table name for the model in lowercase"""
        return self.__name__.lower()[:-3]  # Remove Orm suffix

    id = Column(Integer, primary_key=True)


class Model(DeclarativeBase, PreBase):
    pass


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def drop_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        print('All tables dropped successfully.')
