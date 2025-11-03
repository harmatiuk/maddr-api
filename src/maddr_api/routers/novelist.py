from fastapi import APIRouter, Depends
from maddr_api.config.database import DatabaseSession
from http import HTTPStatus
from maddr_api.models.account import Account
from maddr_api.schemas.novelist import NovelistCreate, NovelistPublic
from maddr_api.security.get_current_user import get_current_user
from maddr_api.services.novelist import NovelistService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

Session = Annotated[AsyncSession, Depends(DatabaseSession.get_session)]

router = APIRouter(prefix="/novelist", tags=["novelist"])


@router.post(
    "/",
    summary="Create a new novelist",
    description="Create a new novelist with the provided data.",
    status_code=HTTPStatus.CREATED,
    response_model=NovelistPublic,
)
async def create_novelist(
    novelist_data: NovelistCreate,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
    current_user: Account = Depends(get_current_user),
) -> NovelistPublic:
    return await NovelistService(session).create_novelist(novelist_data)
