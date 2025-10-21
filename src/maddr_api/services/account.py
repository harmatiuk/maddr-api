from http import HTTPStatus
from fastapi import HTTPException
from maddr_api.schemas.account import AccountCreate
from maddr_api.config.database import DatabaseSession
from sqlalchemy import select
from maddr_api.models.account import Account
from maddr_api.services.main import AccountSearchField
from typing import Union


class AccountCRUD(DatabaseSession):
    """
    CRUD operations for accounts.
    """

    def crete_account(self, account_data: AccountCreate) -> Account:
        """
        Create a new account in the database.
        """

        new_account = Account(
            username=account_data.username,
            email=account_data.email,
            password=account_data.password,
        )

        self.session.add(new_account)
        self.session.commit()
        self.session.refresh(new_account)

        return new_account

    def read_account(
        self, search_field: AccountSearchField, value: Union[str, int]
    ) -> Account | None:
        """
        Read an account from the database by a specific field.
        """

        account_data = self.session.scalar(
            select(Account).where(
                getattr(Account, search_field.value) == value
            )
        )

        return account_data


class AccountService(AccountCRUD):
    """
    Service layer for account operations.
    """

    def create_account(self, account_data: AccountCreate) -> Account:
        """
        Create a new account after checking for existing username and email.
        """

        email_already_exists = self.read_account(
            AccountSearchField.EMAIL, account_data.email
        )

        if email_already_exists:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists.",
            )

        username_already_exists = self.read_account(
            AccountSearchField.USERNAME, account_data.username
        )

        if username_already_exists:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists.",
            )

        new_account = self.crete_account(account_data)

        return new_account
