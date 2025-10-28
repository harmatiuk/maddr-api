from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from maddr_api.config.database import DatabaseSession
from maddr_api.config.settings import Settings
from maddr_api.models.account import Account

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", refreshUrl="refresh")


async def get_current_user(
    session: AsyncSession = Depends(DatabaseSession.get_session),
    token: str = Depends(oauth2_scheme),
) -> Account:
    """
    Retrieve the current authenticated user based on the provided JWT token.
    """
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        subject_username = payload.get("sub")

        if not subject_username:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    account = await session.scalar(
        select(Account).where(Account.username == subject_username)
    )

    if not account:
        raise credentials_exception

    return account
