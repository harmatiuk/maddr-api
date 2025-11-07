from fastapi import APIRouter, Depends
from maddr_api.config.database import DatabaseSession
from http import HTTPStatus
from maddr_api.models.account import Account
from maddr_api.schemas.author import (
    AuthorCreate,
    AuthorMessageResponse,
    AuthorPublic,
)
from maddr_api.security.get_current_user import get_current_user
from maddr_api.services.author import AuthorService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

Session = Annotated[AsyncSession, Depends(DatabaseSession.get_session)]

router = APIRouter(prefix="/author", tags=["author"])


@router.post(
    "/",
    summary="Create a new author",
    description="Create a new author with the provided data.",
    status_code=HTTPStatus.CREATED,
    response_model=AuthorPublic,
)
async def create_author(
    author_data: AuthorCreate,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
    current_user: Account = Depends(get_current_user),
) -> AuthorPublic:
    return await AuthorService(session).create_author(author_data)


@router.get(
    "/{author_id}",
    summary="Get author by ID",
    description="Retrieve author details by their ID.",
    status_code=HTTPStatus.OK,
    response_model=AuthorPublic,
)
async def read_author(
    author_id: int,
    session: Session,
    current_user: Account = Depends(get_current_user),
) -> AuthorPublic:
    return await AuthorService(session).read_author(author_id)


@router.delete(
    "/{author_id}",
    summary="Delete author by ID",
    description="Delete an author by their ID.",
    status_code=HTTPStatus.OK,
    response_model=AuthorMessageResponse,
)
async def delete_author(
    author_id: int,
    session: Session,
    current_user: Account = Depends(get_current_user),
) -> None:
    return await AuthorService(session).delete_author(author_id)
