from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from maddr_api.config.settings import Settings


class DatabaseSession:
    """
    Base service class for database operations.
    """

    engine = create_async_engine(Settings().DATABASE_URL)

    @staticmethod
    async def get_session():
        """
        Provide a database session.
        Use as dependency: Depends(DatabaseSession.get_session)
        """
        async with AsyncSession(
            DatabaseSession.engine, expire_on_commit=False
        ) as session:
            yield session

    def __init__(self, session: AsyncSession):
        self.session = session
