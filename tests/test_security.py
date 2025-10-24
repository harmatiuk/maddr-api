from jwt import decode

from maddr_api.security.access_token import (
    SECRET_KEY,
    ALGORITHM,
    create_access_token,
)


def test_create_access_token():
    data = dict(test="test")

    token = create_access_token(data)

    decoded_data = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_data["test"] == "test"
    assert "exp" in decoded_data
