from maddr_api.config.database import get_sesion


class DatabaseSession(object):
    """
    Base service class for database operations.
    """

    def __init__(self, session: get_sesion):
        self.session = session
