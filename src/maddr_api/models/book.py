from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from .account import table_registry


@table_registry.mapped_as_dataclass
class Book:
    """
    Database model for a book.
    """

    __tablename__ = "book"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    author_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
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
