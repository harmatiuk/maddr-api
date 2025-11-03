from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """
    Base schema for a book.
    """

    title: str
    author_id: int
    publish_year: int


class BookCreate(BookBase):
    """
    Schema for creating a new book in the database.
    """

    pass


class BookPublic(BookBase):
    """
    Public representation of a book.
    """

    id: int


class BookMessageResponse(BaseModel):
    """
    Schema for a message response related to books.
    """

    message: str


class FilterPage(BaseModel):
    """
    Schema for pagination and filtering of books.
    """
    publish_year: int | None = None
    title: str | None = None
    limit: int = Field(20, ge=1)
    skip: int = Field(0, ge=0)
