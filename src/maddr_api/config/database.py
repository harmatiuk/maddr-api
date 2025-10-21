from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from maddr_api.config.settings import Settings


class DatabaseSession:
    """
    Base service class for database operations.
    """

    engine = create_engine(
        Settings().DATABASE_URL, connect_args={"check_same_thread": False}
    )

    @staticmethod
    def get_sesion():
        """
        Provide a database session.
        Use as dependency: Depends(DatabaseSession.get_sesion)
        """
        with Session(DatabaseSession.engine) as session:
            yield session

    def __init__(self, session: Session):
        self.session = session
