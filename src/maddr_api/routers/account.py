from fastapi import APIRouter, Depends
from maddr_api.config.database import DatabaseSession
from http import HTTPStatus
from maddr_api.schemas.account import (
    AccountCreate,
    AccountPublic,
    AccountMessageResponse,
)
from maddr_api.services.account import AccountService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

Session = Annotated[AsyncSession, Depends(DatabaseSession.get_session)]

router = APIRouter(prefix="/account", tags=["account"])


@router.post(
    "/",
    summary="Create a new account",
    description="Create a new account with the provided data.",
    status_code=HTTPStatus.CREATED,
    response_model=AccountPublic,
)
async def create_account(
    account_data: AccountCreate,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
) -> AccountPublic:
    return await AccountService(session).create_account(account_data)


@router.get(
    "/{account_id}",
    summary="Read an account",
    description="Retrieve an account by its ID.",
    status_code=HTTPStatus.OK,
    response_model=AccountPublic,
)
async def read_account(
    account_id: int,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
) -> AccountPublic:
    return await AccountService(session).read_account(
        search_field="id", value=account_id
    )


@router.put(
    "/{account_id}",
    summary="Update an account",
    description="Update an existing account by its ID.",
    status_code=HTTPStatus.OK,
    response_model=AccountPublic,
)
async def update_account(
    account_id: int,
    account_data: AccountCreate,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
) -> AccountPublic:
    return await AccountService(session).update_account(account_id, account_data)


@router.delete(
    "/{account_id}",
    summary="Delete an account",
    description="Delete an account by its ID.",
    status_code=HTTPStatus.OK,
    response_model=AccountMessageResponse,
)
async def delete_account(
    account_id: int,
    session: DatabaseSession = Depends(DatabaseSession.get_session),
) -> AccountMessageResponse:
    return await AccountService(session).delete_account(account_id)
