from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .account import table_registry


if TYPE_CHECKING:
    from .book import Book


@table_registry.mapped_as_dataclass
class Author:
    """
    Database model for a author.
    """

    __tablename__ = "author"

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

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")
