from pydantic import BaseModel


class authorBase(BaseModel):
    """
    Base schema for a author.
    """

    id: int


class authorCreate(BaseModel):
    """
    Schema for creating a new author in the database.
    """

    name: str


class authorPublic(authorCreate):
    """
    Public representation of a author.
    """

    pass


class authorMessageResponse(BaseModel):
    """
    Schema for a message response related to authors.
    """

    message: str
