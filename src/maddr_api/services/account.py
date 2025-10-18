from maddr_api.schemas.account import AccountCreate
from maddr_api.services.main import AppCRUD
from sqlalchemy import select
from maddr_api.models.account import Account


class AccountService(AppCRUD):
    def create_account(self, account_data: AccountCreate) -> Account:
        check_if_existing_account = self.session.scalar(
            select(Account).where(
                (Account.username == account_data.username)
                | (Account.email == account_data.email)
            )
        )

        if check_if_existing_account:
            if account_data.username == check_if_existing_account.username:
                raise ValueError("Username already exists.")
            if account_data.email == check_if_existing_account.email:
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
