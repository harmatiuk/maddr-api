from enum import Enum


class AccountSearchField(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    ID = "id"
