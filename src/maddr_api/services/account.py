from maddr_api.schemas.account import AccountCreate
from maddr_api.services.main import AppCRUD
from sqlalchemy import select
from maddr_api.models.account import Account


class AccountService(AppCRUD):
    def create_account(self, account_data: AccountCreate) -> Account:
        account_exists = self.session.scalar(
            select(Account).where(
                (Account.username == account_data.username)
                | (Account.email == account_data.email)
            )
        )

        if account_exists:
            if account_data.username == account_exists.username:
                raise ValueError("Username already exists.")
            if account_data.email == account_exists.email:
                raise ValueError("Email already exists.")

        new_account = Account(
            username=account_data.username,
            email=account_data.email,
            password=account_data.password,
        )
        self.session.add(new_account)
        self.session.commit()
        self.session.refresh(new_account)
        return new_account
