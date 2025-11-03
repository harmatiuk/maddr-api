from datetime import datetime

from maddr_api.models.book import Book
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .account import table_registry


@table_registry.mapped_as_dataclass
class Novelist:
    """
    Database model for a novelist.
    """

    __tablename__ = "novelist"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    books: Mapped[list["Book"]]  = relationship(
        init=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
