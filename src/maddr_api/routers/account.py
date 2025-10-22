from fastapi import APIRouter, Depends
from maddr_api.config.database import DatabaseSession
from http import HTTPStatus
from maddr_api.schemas.account import AccountCreate, AccountPublic, AccountMessageResponse
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
    account_data: AccountCreate,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
) -> AccountPublic:
    return AccountService(session).create_account(account_data)


@router.delete(
    "/{account_id}",
    summary="Delete an account",
    description="Delete an account by its ID.",
    status_code=HTTPStatus.OK,
    response_model=AccountMessageResponse,
)
def delete_account(
    account_id: int,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
) -> AccountMessageResponse:
    return AccountService(session).delete_account(account_id)