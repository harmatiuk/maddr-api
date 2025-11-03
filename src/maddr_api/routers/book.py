from fastapi import APIRouter, Depends, Query
from maddr_api.config.database import DatabaseSession
from http import HTTPStatus
from maddr_api.models.account import Account
from maddr_api.schemas.book import BookCreate, BookPublic, FilterPage
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


@router.get(
    "/{book_id}",
    summary="Get book by ID",
    description="Retrieve a book by its ID.",
    status_code=HTTPStatus.OK,
    response_model=BookPublic,
)
async def read_book(
    book_id: int,
    session: Session,
    current_user: Account = Depends(get_current_user),
) -> BookPublic:
    return await BookService(session).read_book(book_id)


@router.get(
    "/",
    summary="Get all books with optional filtering by title and publish year",
    description="Retrieve a list of all books.",
    status_code=HTTPStatus.OK,
    response_model=list[BookPublic],
)
async def read_all_books(
    session: Session,
    filter_books: Annotated[FilterPage, Query()],
    current_user: Account = Depends(get_current_user),
) -> list[BookPublic]:
    return await BookService(session).read_all_books(
        title=filter_books.title,
        publish_year=filter_books.publish_year,
        skip=filter_books.skip,
        limit=filter_books.limit,
    )
