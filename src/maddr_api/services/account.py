from http import HTTPStatus
from fastapi import HTTPException
from maddr_api.schemas.account import AccountCreate
from maddr_api.services.main import DatabaseSession
from sqlalchemy import select
from maddr_api.models.account import Account


class AccountService(DatabaseSession):
    """
    Service class for account operations.
    """

    def create_account(self, account_data: AccountCreate) -> Account:
        """
        Create a new account in the database.
        """

        account_exists = self.session.scalar(
            select(Account).where(
                (Account.username == account_data.username)
                | (Account.email == account_data.email)
            )
        )

        if account_exists:
            if account_data.username == account_exists.username:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail="Username already exists.",
                )

            if account_data.email == account_exists.email:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail="Email already exists.",
                )

        new_account = Account(
            username=account_data.username,
            email=account_data.email,
            password=account_data.password,
        )
        self.session.add(new_account)
        self.session.commit()
        self.session.refresh(new_account)
        return new_account
