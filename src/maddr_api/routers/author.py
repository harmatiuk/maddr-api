from fastapi import APIRouter, Depends
from maddr_api.config.database import DatabaseSession
from http import HTTPStatus
from maddr_api.models.account import Account
from maddr_api.schemas.author import authorCreate, authorPublic
from maddr_api.security.get_current_user import get_current_user
from maddr_api.services.author import authorService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

Session = Annotated[AsyncSession, Depends(DatabaseSession.get_session)]

router = APIRouter(prefix="/author", tags=["author"])


@router.post(
    "/",
    summary="Create a new author",
    description="Create a new author with the provided data.",
    status_code=HTTPStatus.CREATED,
    response_model=authorPublic,
)
async def create_author(
    author_data: authorCreate,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
    current_user: Account = Depends(get_current_user),
) -> authorPublic:
    return await authorService(session).create_author(author_data)
