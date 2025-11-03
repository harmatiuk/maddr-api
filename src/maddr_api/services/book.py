from fastapi import HTTPException
from maddr_api.schemas.book import BookCreate, BookPublic
from maddr_api.models.book import Book
from maddr_api.services.main import BaseCRUD
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from http import HTTPStatus
from maddr_api.utils.sanitization import sanitization_string


class BookService(BaseCRUD[Book, BookCreate]):
    """
    Service layer for book operations.
    """

    def __init__(self, session: Session):
        super().__init__(model=Book, session=session)

    async def create_book(self, book_data: BookCreate) -> Book:
        """
        Create a new book in the database.
        """

        book_data.title = sanitization_string(book_data.title)

        existing_book = await self.read(
            search_field="title", value=book_data.title
        )

        if existing_book:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="A book with this title already exists.",
            )

        return await self.create(book_data)

    async def read_book(self, book_id: int) -> Book:
        """
        Read a book by its ID.
        """

        book = await self.read(search_field="id", value=book_id)

        if not book:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Book not found.",
            )

        return book

    async def read_all_books(
        self, skip: int, limit: int
    ) -> dict[str, list[BookPublic]]:
        """
        Read all books from the database.
        """

        query = await self.session.scalars(
            select(self.model).offset(skip).limit(limit)
        )

        books = query.all()

        if not books:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="No books found.",
            )

        return books
