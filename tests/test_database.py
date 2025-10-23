import pytest
from maddr_api.models.account import Account
from sqlalchemy import select
from dataclasses import asdict


@pytest.mark.asyncio
async def test_create_account_in_database(session, mock_db_time):
    with mock_db_time(model=Account) as time:
        new_account = Account(
            username="test_criando_account_in_db",
            email="test_criando_account_in_db@gmail.com",
            password="test_criando_account_in_db",
        )

        session.add(new_account)
        await session.commit()

    account = await session.scalar(
        select(Account).where(Account.username == "test_criando_account_in_db")
    )

    data_expect = dict(
        id=1,
        username="test_criando_account_in_db",
        password="test_criando_account_in_db",
        email="test_criando_account_in_db@gmail.com",
        created_at=time,
        updated_at=time,
    )

    assert asdict(account) == data_expect
