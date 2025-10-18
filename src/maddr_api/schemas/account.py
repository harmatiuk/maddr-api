from pydantic import BaseModel, EmailStr


class AccountBase(BaseModel):
    username: str
    email: EmailStr


class AccountPublic(AccountBase):
    id: int


class AccountCreate(AccountBase):
    password: str
