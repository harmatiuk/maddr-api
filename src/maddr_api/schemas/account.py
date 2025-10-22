from pydantic import BaseModel, EmailStr


class AccountBase(BaseModel):
    """
    Base schema for an account.
    """

    username: str
    email: EmailStr


class AccountPublic(AccountBase):
    """
    Public representation of an account.
    """

    id: int


class AccountCreate(AccountBase):
    """
    Schema for creating a new account in the database.
    """

    password: str


class AccountMessageResponse(BaseModel):
    """
    Schema for a message response.
    """

    message: str
