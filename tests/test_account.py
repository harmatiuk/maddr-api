from http import HTTPStatus


def test_successful_account_creation(client):
    """
    Test creating a new account successfully.
    """

    account_data = dict(
        username="test_successful_account_creation",
        email="test_successful_account_creation@gmail.com",
        password="testpass",
    )

    response = client.post("/account/", json=account_data)

    expected_response = account_data

    expected_response.pop("password")
    expected_response.update(dict(id=1))

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected_response


def test_create_account_with_existing_username(client, account):
    """
    Test creating an account with an existing username.
    """

    account_data = dict(
        username=account.username,
        email="test_create_account_existing_username@gmail.com",
        password="testpass",
    )

    response = client.post("/account/", json=account_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists."}

def test_create_account_with_existing_email(client, account):
    """
    Test creating an account with an existing email.
    """

    account_data = dict(
        username="test_create_account_with_existing_email",
        email=account.email,
        password="testpass",
    )

    response = client.post("/account/", json=account_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists."}