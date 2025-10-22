from enum import Enum
from typing import Generic, TypeVar, Type, Optional, Any
from sqlalchemy import select
from sqlalchemy.orm import Session
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

    def create(self, data: CreateSchemaType) -> ModelType:
        """
        Create a new record in the database.
        """

        obj_data = data.model_dump()
        db_data = self.model(**obj_data)

        self.session.add(db_data)
        self.session.commit()
        self.session.refresh(db_data)

        return db_data

    def read(self, search_field: str, value: Any) -> Optional[ModelType]:
        """
        Read a record from the database by a specific field.
        """

        record = self.session.scalar(
            select(self.model).where(
                getattr(self.model, search_field) == value
            )
        )

        return record

    def update(
        self, id_column: str, value: Any, update_data: UpdateSchemaType
    ) -> Optional[ModelType]:
        """
        Update a record in the database by a specific id field.
        """

        record = self.read(search_field=id_column, value=value)

        if not record:
            return False

        for field, field_value in update_data.model_dump().items():
            setattr(record, field, field_value)

        self.session.commit()
        self.session.refresh(record)

        return record

    def delete(self, id_column: str, value: Any) -> bool:
        """
        Delete a record from the database by a specific id field.
        """

        try:
            record = self.read(search_field=id_column, value=value)
            self.session.delete(record)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False


class AccountSearchField(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    ID = "id"
