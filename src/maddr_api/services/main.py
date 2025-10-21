from enum import Enum
from typing import Generic, TypeVar, Type, Optional, Any
from sqlalchemy import select
from sqlalchemy.orm import Session


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")


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


class AccountSearchField(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    ID = "id"
