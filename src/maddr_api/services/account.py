from http import HTTPStatus
from fastapi import HTTPException
from maddr_api.schemas.account import AccountCreate
from maddr_api.models.account import Account
from maddr_api.services.main import AccountSearchField
from maddr_api.services.main import BaseCRUD
from sqlalchemy.orm import Session


class AccountService(BaseCRUD[Account, AccountCreate]):
    """
    Service layer for account operations.
    """

    def __init__(self, session: Session):
        super().__init__(model=Account, session=session)

    def create_account(self, account_data: AccountCreate) -> Account:
        """
        Create a new account after checking for existing username and email.
        """

        for field, message in [
            (AccountSearchField.USERNAME, "Username already exists."),
            (AccountSearchField.EMAIL, "Email already exists."),
        ]:
            existing_account = self.read(
                field.value, getattr(account_data, field.value)
            )
            if existing_account:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=message,
                )

        return self.create(account_data)
