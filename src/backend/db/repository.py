from typing import Any, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import Model
from core.logging import get_logger

logger = get_logger(__name__)
ModelType = TypeVar('ModelType', bound=Model)


# Type hints for better IDE support
ModelType = TypeVar('ModelType')
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class SQLAlchemyRepository(Generic[ModelType, SchemaType]):
    """
    Base repository class for common database operations.
    Now instance-based to work with DBManager's lifecycle.
    """

    model: Type[ModelType] = None
    schema: Type[SchemaType] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, model_data: SchemaType) -> int:
        """
        Create a new record.
        """
        try:
            model_dict = model_data.model_dump()
            model_obj = self.model(**model_dict)
            self.session.add(model_obj)

            await self.session.flush()
            return model_obj.id

        except IntegrityError as e:
            raise ValueError(f'Record already exists: {e}') from e
        except Exception as e:
            raise RuntimeError('Internal database error') from e

    async def find_all(self) -> List[SchemaType]:
        """Retrieve all records and auto-validate into Pydantic schemas."""
        try:
            query = select(self.model)
            result = await self.session.execute(query)
            model_objs = result.scalars().all()

            if self.schema:
                return [self.schema.model_validate(obj) for obj in model_objs]
            return model_objs
        except SQLAlchemyError as e:
            raise RuntimeError('Failed to fetch records') from e

    async def get_one_by_field(
        self, attr_name: str, attr_value: Any
    ) -> Optional[SchemaType]:
        """Generic filter for a single record."""
        query = select(self.model).where(
            getattr(self.model, attr_name) == attr_value
        )
        result = await self.session.execute(query)
        obj = result.scalars().first()

        if obj and self.schema:
            return self.schema.model_validate(obj)
        return obj

    async def update(self, db_obj: ModelType, obj_in: SchemaType) -> ModelType:
        """Update an object in the current session context."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def delete(self, db_obj: ModelType) -> None:
        """Mark an object for deletion."""
        try:
            await self.session.delete(db_obj)
            await self.session.flush()
        except SQLAlchemyError as e:
            raise RuntimeError('Failed to delete record') from e

    async def add_one_from_dict(self, data_dict: dict) -> int:
        """Create a new record from a dictionary."""
        try:
            model_obj = self.model(**data_dict)
            self.session.add(model_obj)
            await self.session.flush()
            return model_obj.id
        except IntegrityError as e:
            raise ValueError(f'Record already exists: {e}') from e
        except Exception as e:
            raise RuntimeError('Internal database error') from e
