from fastapi import APIRouter, Depends
from maddr_api.config.database import get_sesion
from http import HTTPStatus
from maddr_api.schemas.account import AccountCreate, AccountPublic
from maddr_api.services.account import AccountService

router = APIRouter(prefix="/account", tags=["account"])


@router.post(
    "/",
    summary="Create a new account",
    description="Create a new account with the provided data.",
    status_code=HTTPStatus.CREATED,
    response_model=AccountPublic,
)
async def create_account(account_data: AccountCreate, db=Depends(get_sesion)):
    new_account = AccountService(db).create_account(account_data)
    if new_account:
        return new_account
