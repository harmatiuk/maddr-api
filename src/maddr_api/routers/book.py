from fastapi import APIRouter, Depends
from maddr_api.config.database import DatabaseSession
from http import HTTPStatus
from maddr_api.models.account import Account
from maddr_api.schemas.book import (
    BookCreate,
    BookPublic,
)
from maddr_api.security.get_current_user import get_current_user
from maddr_api.services.book import BookService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

Session = Annotated[AsyncSession, Depends(DatabaseSession.get_session)]

router = APIRouter(prefix="/book", tags=["book"])


@router.post(
    "/",
    summary="Create a new book",
    description="Create a new book with the provided data.",
    status_code=HTTPStatus.CREATED,
    response_model=BookPublic,
)
async def create_book(
    book_data: BookCreate,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
    current_user: Account = Depends(get_current_user),
) -> BookPublic:
    return await BookService(session).create_book(book_data)
