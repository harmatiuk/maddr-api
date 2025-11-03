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
        self,
        title: str | None,
        publish_year: int | None,
        skip: int,
        limit: int,
    ) -> dict[str, list[BookPublic]]:
        """
        Read all books with optional filtering by title and publish year.
        """

        filter_conditions = []

        if title:
            filter_conditions.append(self.model.title.ilike(f"%{title}%"))
        
        if publish_year:
            filter_conditions.append(self.model.publish_year == publish_year)
        
        query = select(self.model)
    
        if filter_conditions:
            query = query.where(*filter_conditions)
        
        query = query.offset(skip).limit(limit)
        result = await self.session.scalars(query)
        
        books = result.all()

        if not books:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="No books found.",
            )

        return books
