import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy import event
from contextlib import contextmanager
from datetime import datetime
from maddr_api.app import app
from maddr_api.config.database import DatabaseSession
from maddr_api.models.account import Account, table_registry
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from maddr_api.security.hash_password import get_password_hash


@pytest_asyncio.fixture
async def session():
    """
    Create a new database session for a test.
    """

    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(session):
    """
    Create a new FastAPI test client for a test.
    """

    def override_get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[DatabaseSession.get_session] = (
            override_get_session
        )
        yield client
        app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 5, 16)):
    """
    Context manager to mock database time for testing.
    """

    def fake_time(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "updated_at"):
            target.updated_at = time

    event.listen(model, "before_insert", fake_time)

    yield time

    event.remove(model, "before_insert", fake_time)


@pytest.fixture
def mock_db_time():
    """
    Fixture to mock database time for testing.
    """

    return _mock_db_time


@pytest_asyncio.fixture
async def account(session):
    """
    Create a sample account in the database for testing.
    """

    new_account = Account(
        username="testuser",
        email="test@gmail.com",
        password=get_password_hash("testpass"),
    )
    session.add(new_account)
    await session.commit()
    await session.refresh(new_account)

    return new_account
