from __future__ import annotations
from datetime import datetime

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .account import table_registry


if TYPE_CHECKING:
    from .author import Author


@table_registry.mapped_as_dataclass
class Book:
    """
    Database model for a book.
    """

    __tablename__ = "book"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(nullable=False)
    publish_year: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    author: Mapped["Author"] = relationship(
        "Author", back_populates="books", init=False
    )
