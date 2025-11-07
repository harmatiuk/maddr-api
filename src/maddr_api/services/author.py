from fastapi import HTTPException
from maddr_api.schemas.author import AuthorCreate, AuthorMessageResponse
from maddr_api.models.author import Author
from maddr_api.services.main import BaseCRUD
from sqlalchemy.ext.asyncio import AsyncSession as Session
from http import HTTPStatus
from maddr_api.utils.sanitization import sanitization_string


class AuthorService(BaseCRUD[Author, AuthorCreate]):
    """
    Service layer for author operations.
    """

    def __init__(self, session: Session):
        super().__init__(model=Author, session=session)

    async def create_author(self, author_data: AuthorCreate) -> Author:
        """
        Create a new author in the database.
        """

        author_data.name = sanitization_string(author_data.name)

        existing_author = await self.read(
            search_field="name", value=author_data.name
        )

        if existing_author:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="An author with this name already exists.",
            )

        return await self.create(author_data)

    async def read_author(self, author_id: int) -> Author:
        """
        Read a author by its ID.
        """

        author = await self.read(search_field="id", value=author_id)

        if not author:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Author not found.",
            )

        return author

    async def delete_author(self, author_id: int) -> AuthorMessageResponse:
        """
        Delete an author by its ID.
        """

        author = await self.read(search_field="id", value=author_id)

        if not author:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Author not found.",
            )

        await self.delete(id_column="id", value=author_id)

        return AuthorMessageResponse(message="Author deleted successfully.")
