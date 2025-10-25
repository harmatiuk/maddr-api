from http import HTTPStatus


def test_create_token_successful(client, account):
    """
    Test generating an access token successfully.
    """

    form_data = dict(username=account.username, password="testpass")

    response = client.post(
        "/token/",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


def test_create_token_invalid_password(client, account):
    """
    Test generating an access token with invalid credentials.
    """

    form_data = dict(username=account.username, password="wrongpass")

    response = client.post(
        "/token/",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response_data = response.json()
    assert response_data["detail"] == "Incorrect username or password."


def test_create_token_nonexistent_user(client):
    """
    Test generating an access token for a nonexistent user.
    """

    form_data = dict(username="nonexistent", password="somepass")

    response = client.post(
        "/token/",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response_data = response.json()
    assert response_data["detail"] == "Incorrect username or password."
