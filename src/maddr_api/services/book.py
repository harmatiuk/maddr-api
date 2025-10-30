from maddr_api.schemas.book import BookCreate
from maddr_api.models.book import Book
from maddr_api.services.main import BaseCRUD
from sqlalchemy.ext.asyncio import AsyncSession as Session


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
        return await self.create(book_data)
