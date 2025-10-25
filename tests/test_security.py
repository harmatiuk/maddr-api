from jwt import decode

from maddr_api.security.access_token import (
    create_access_token,
)
from maddr_api.config.settings import Settings

settings = Settings()

def test_create_access_token():
    data = dict(test="test")

    token = create_access_token(data)

    decoded_data = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded_data["test"] == "test"
    assert "exp" in decoded_data
