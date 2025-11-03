from fastapi import HTTPException
from maddr_api.schemas.novelist import NovelistCreate
from maddr_api.models.novelist import Novelist
from maddr_api.services.main import BaseCRUD
from sqlalchemy.ext.asyncio import AsyncSession as Session
from http import HTTPStatus
from maddr_api.utils.sanitization import sanitization_string


class NovelistService(BaseCRUD[Novelist, NovelistCreate]):
    """
    Service layer for novelist operations.
    """

    def __init__(self, session: Session):
        super().__init__(model=Novelist, session=session)

    async def create_novelist(self, novelist_data: NovelistCreate) -> Novelist:
        """
        Create a new novelist in the database.
        """

        novelist_data.name = sanitization_string(novelist_data.name)

        existing_novelist = await self.read(
            search_field="name", value=novelist_data.name
        )

        if existing_novelist:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="A novelist with this name already exists.",
            )

        return await self.create(novelist_data)

    async def read_novelist(self, novelist_id: int) -> Novelist:
        """
        Read a novelist by its ID.
        """

        novelist = await self.read(search_field="id", value=novelist_id)

        if not novelist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Novelist not found.",
            )

        return novelist
