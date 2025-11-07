from pydantic import BaseModel


class AuthorCreate(BaseModel):
    """
    Schema for creating a new author in the database.
    """

    name: str


class AuthorPublic(AuthorCreate):
    """
    Public representation of an author.
    """

    id: int


class AuthorMessageResponse(BaseModel):
    """
    Schema for a message response related to authors.
    """

    message: str
