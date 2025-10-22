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
    assert (
        response.json()["detail"][0]["msg"]
        == "value is not a valid email address: An email address must have an @-sign."
    )


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
        password="testpass",
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
        email="test_create_account_with_missing_password_field@gmail.com",
    )

    response = client.post("/account/", json=account_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Field required"


def test_read_account_successfully(client, account):
    """
    Test reading an existing account successfully.
    """

    response = client.get(f"/account/{account.id}")

    expected_response = dict(
        id=account.id,
        username=account.username,
        email=account.email,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response

def test_read_nonexistent_account(client):
    """
    Test reading a non-existent account.
    """

    response = client.get("/account/9999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Account not found."}


def test_update_account_successfully(client, account):
    """
    Test updating an existing account successfully.
    """

    updated_data = dict(
        username="updated_username",
        email="updated_email@example.com",
        password="updated_password",
    )

    response = client.put(f"/account/{account.id}", json=updated_data)

    expected_response = dict(
        id=account.id,
        username=updated_data["username"],
        email=updated_data["email"],
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response

def test_update_nonexistent_account(client):
    """
    Test updating a non-existent account.
    """

    updated_data = dict(
        username="nonexistent_username",
        email="nonexistent_email@example.com",
        password="nonexistent_password",
    )

    response = client.put("/account/9999", json=updated_data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Account not found."}


def test_delete_account_successfully(client, account):
    """
    Test deleting an existing account successfully.
    """

    response = client.delete(f"/account/{account.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Account deleted successfully."}

def test_delete_nonexistent_account(client):
    """
    Test deleting a non-existent account.
    """

    response = client.delete("/account/9999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Account not found."}