from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from .account import table_registry


@table_registry.mapped_as_dataclass
class author:
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
