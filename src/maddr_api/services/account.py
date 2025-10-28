from http import HTTPStatus
from fastapi import HTTPException
from maddr_api.schemas.account import AccountCreate, AccountMessageResponse
from maddr_api.models.account import Account
from maddr_api.services.main import AccountSearchField
from maddr_api.services.main import BaseCRUD
from maddr_api.security.hash_password import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession as Session


class AccountService(BaseCRUD[Account, AccountCreate]):
    """
    Service layer for account operations.
    """

    def __init__(self, session: Session):
        super().__init__(model=Account, session=session)

    async def create_account(self, account_data: AccountCreate) -> Account:
        """
        Create a new account after checking for existing username and email.
        """

        for field, message in [
            (AccountSearchField.USERNAME, "Username already exists."),
            (AccountSearchField.EMAIL, "Email already exists."),
        ]:
            existing_account = await self.read(
                field.value, getattr(account_data, field.value)
            )
            if existing_account:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=message,
                )

        account_data.password = get_password_hash(account_data.password)

        return await self.create(account_data)

    async def read_account(self, search_field: str, value: str) -> Account:
        """
        Read an account by a specific field.
        """

        account = await self.read(search_field=search_field, value=value)

        if not account:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Account not found.",
            )

        return account

    async def update_account(
        self,
        account_id: int,
        account_data: AccountCreate,
        current_user: Account,
    ) -> Account:
        """
        Update an existing account by its ID.
        """

        account_data.password = get_password_hash(account_data.password)

        account = await self.update(
            id_column="id",
            value=account_id,
            update_data=account_data,
        )

        if not account:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Account not found.",
            )

        if current_user.id != account_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Not authorized to update this account.",
            )

        return account

    async def delete_account(
        self, account_id: int, current_user: Account
    ) -> AccountMessageResponse:
        """
        Delete an account by its ID.
        """

        success = await self.delete(id_column="id", value=account_id)
        if not success:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Account not found.",
            )

        if current_user.id != account_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Not authorized to delete this account.",
            )

        return AccountMessageResponse(message="Account deleted successfully.")
