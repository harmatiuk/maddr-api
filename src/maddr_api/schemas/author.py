from pydantic import BaseModel


class AuthorBase(BaseModel):
    """
    Base schema for a author.
    """

    id: int


class AuthorCreate(AuthorBase):
    """
    Schema for creating a new author in the database.
    """

    name: str


class AuthorPublic(AuthorCreate):
    """
    Public representation of a author.
    """

    pass


class authorMessageResponse(BaseModel):
    """
    Schema for a message response related to authors.
    """

    message: str
