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


def test_create_account_with_wrong_email_format(client):
    """
    Test creating an account with an invalid email format.
    """

    account_data = dict(
        username="test_create_account_with_wrong_email_format",
        email="invalid-email-format",
        password="testpass",
    )

    response = client.post("/account/", json=account_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "value is not a valid email address: An email address must have an @-sign."

def test_create_account_with_missing_email_field(client):
    """
    Test creating an account with missing email field.
    """
    
    account_data = dict(
        username="test_create_account_with_missing_email_field",
        password="testpass",
    )

    response = client.post("/account/", json=account_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_create_account_with_missing_username_field(client):
    """
    Test creating an account with missing username field.
    """

    account_data = dict(
        email="test_create_account_with_missing_username_field@gmail.com",
        password="testpass"
    )
    
    response = client.post("/account/", json=account_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_create_account_with_missing_password_field(client):
    """
    Test creating an account with missing password field.
    """

    account_data = dict(
        username="test_create_account_with_missing_password_field",
        email="test_create_account_with_missing_password_field@gmail.com"
    )

    response = client.post("/account/", json=account_data)
    
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Field required"