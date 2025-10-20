from maddr_api.config.database import get_sesion
from enum import Enum


class DatabaseSession(object):
    """
    Base service class for database operations.
    """

    def __init__(self, session: get_sesion):
        self.session = session


class AccountSearchField(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    ID = "id"
