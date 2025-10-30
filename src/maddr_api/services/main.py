import re
from enum import Enum
from typing import Generic, TypeVar, Type, Optional, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.exc import SQLAlchemyError

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseCRUD(Generic[ModelType, CreateSchemaType]):
    """
    Generic CRUD operations for any model.
    """

    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    async def create(self, data: CreateSchemaType) -> ModelType:
        """
        Create a new record in the database.
        """

        obj_data = data.model_dump()
        db_data = self.model(**obj_data)

        self.session.add(db_data)
        await self.session.commit()
        await self.session.refresh(db_data)

        return db_data

    async def read(self, search_field: str, value: Any) -> Optional[ModelType]:
        """
        Read a record from the database by a specific field.
        """

        record = await self.session.scalar(
            select(self.model).where(
                getattr(self.model, search_field) == value
            )
        )

        return record

    async def update(
        self, id_column: str, value: Any, update_data: UpdateSchemaType
    ) -> Optional[ModelType]:
        """
        Update a record in the database by a specific id field.
        """

        record = await self.read(search_field=id_column, value=value)

        if not record:
            return False

        for field, field_value in update_data.model_dump().items():
            setattr(record, field, field_value)

        await self.session.commit()
        await self.session.refresh(record)

        return record

    async def delete(self, id_column: str, value: Any) -> bool:
        """
        Delete a record from the database by a specific id field.
        """

        try:
            record = await self.read(search_field=id_column, value=value)
            await self.session.delete(record)
            await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            return False
        
    def sanitization_string(self, input_string:str) -> str:
        """
        Sanitize input strings by removing special characters and normalizing whitespace.
        """
        sanitized = re.sub(r'[^a-zA-Z0-9 ]', '', input_string)
        sanitized = sanitized.strip().lower()
        sanitized = re.sub(r'\s+', ' ', sanitized)

        return sanitized


class AccountSearchField(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    ID = "id"
