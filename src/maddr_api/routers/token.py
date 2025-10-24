from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus
from maddr_api.schemas.token import Token
from maddr_api.config.database import DatabaseSession
from maddr_api.services.token import TokenService
from typing import Annotated


Session = Annotated[DatabaseSession, Depends(DatabaseSession.get_session)]

router = APIRouter(prefix="/token", tags=["token"])


@router.post(
    "/",
    summary="Generate access token",
    description="Generate an access token for a user.",
    status_code=HTTPStatus.OK,
    response_model=Token,
)
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: DatabaseSession = Depends(DatabaseSession.get_session),
) -> Token:
    return await TokenService(session).create_access_token(form_data)
