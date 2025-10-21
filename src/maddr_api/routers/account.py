from fastapi import APIRouter, Depends
from maddr_api.config.database import DatabaseSession
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
def create_account(
    account_data: AccountCreate, db=Depends(DatabaseSession.get_sesion)
) -> AccountPublic | ValueError:
    new_account = AccountService(db).create_account(account_data)

    return new_account
