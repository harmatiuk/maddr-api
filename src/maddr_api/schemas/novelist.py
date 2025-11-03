from pydantic import BaseModel, Field

class NovelistBase(BaseModel):
    """
    Base schema for a novelist.
    """

    id: int


class NovelistCreate(BaseModel):
    """
    Schema for creating a new novelist in the database.
    """

    name: str

class NovelistPublic(NovelistCreate):
    """
    Public representation of a novelist.
    """

    pass


class NovelistMessageResponse(BaseModel):
    """
    Schema for a message response related to novelists.
    """

    message: str