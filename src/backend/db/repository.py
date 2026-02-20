from typing import List, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.core.base import AbstractRepository
from backend.db.database import Model, new_session
from core.logging import get_logger
from core.messages import DbErrorMessages, DbLogMessages

logger = get_logger(__name__)
ModelType = TypeVar('ModelType', bound=Model)


class SQLAlchemyRepository(AbstractRepository):
    """Base repository class for common database operations."""

    model = None

    @classmethod
    async def add_one(cls, model_data: BaseModel) -> int:
        """
        Create a new record in the database.

        Raises:
            ValueError: If unique constraints are violated.
            RuntimeError: On database or internal system failures.
        """
        async with new_session() as session:
            try:
                model_dict = model_data.model_dump()
                model_obj = cls.model(**model_dict)
                session.add(model_obj)
                await session.flush()
                await session.commit()
                logger.info(DbLogMessages.COMMIT_SUCCESS, model_obj.id)
                return model_obj.id
            except IntegrityError as e:
                await session.rollback()
                logger.warning(DbLogMessages.INTEGRITY_ERROR, model_data, e)
                raise ValueError(
                    DbErrorMessages.ALREADY_EXISTS.format(
                        model=cls.model, data=model_data
                    )
                ) from e
            except Exception as e:
                await session.rollback()
                logger.exception(DbLogMessages.UNEXPECTED_ERROR, 'add', e)
                raise RuntimeError(DbErrorMessages.INTERNAL_ERROR) from e

    @classmethod
    async def find_all(cls) -> List[ModelType]:
        """
        Retrieve all records for the current model.

        Returns:
            List of model instances or an empty list.
        """
        async with new_session() as session:
            try:
                query = select(cls.model)
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                logger.error(DbLogMessages.FETCH_ERROR, str(e))
                raise RuntimeError(DbErrorMessages.INTERNAL_ERROR) from e

    @classmethod
    async def get_one(cls, record_id: int) -> ModelType:
        """
        Retrieve a single record by its unique ID.

        Raises:
            ValueError: If record is not found.
            RuntimeError: On database execution errors.
        """
        async with new_session() as session:
            try:
                query = select(cls.model).where(cls.model.id == record_id)
                result = await session.execute(query)
                model_obj = result.scalar_one_or_none()
                if model_obj is None:
                    logger.warning(
                        DbLogMessages.NOT_FOUND, cls.model, record_id
                    )
                    raise ValueError(
                        DbErrorMessages.NOT_FOUND.format(
                            model=cls.model, id=record_id
                        )
                    )
                return model_obj
            except SQLAlchemyError as e:
                logger.error(DbLogMessages.FETCH_ERROR, str(e))
                raise RuntimeError(DbErrorMessages.INTERNAL_ERROR) from e

    @classmethod
    async def update(cls, db_obj: ModelType, obj_in: BaseModel) -> ModelType:
        """
        Update an existing database object with new data.

        Returns:
            The updated model instance.
        """
        async with new_session() as session:
            obj_data = jsonable_encoder(db_obj)
            update_data = obj_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    @classmethod
    async def delete(cls, db_obj: ModelType) -> ModelType:
        """
        Remove a record from the database.

        Returns:
            The deleted model instance.
        """
        async with new_session() as session:
            await session.delete(db_obj)
            await session.commit()
            return db_obj
