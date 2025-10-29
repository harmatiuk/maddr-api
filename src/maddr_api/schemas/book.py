from pydantic import BaseModel

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