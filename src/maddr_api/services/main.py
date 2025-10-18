from maddr_api.config.database import get_sesion as Session


class DatabaseService(object):
    def __init__(self, session: Session):
        self.session = session


class AppService(DatabaseService): ...


class AppCRUD(DatabaseService): ...
