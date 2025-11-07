from http import HTTPStatus


def test_successful_author_creation(client, token):
    """
    Test creating a new author successfully.
    """
    headers = {"Authorization": f"Bearer {token}"}
    author_data = dict(
        name="Test Author Name",
    )

    response = client.post("/author/", json=author_data, headers=headers)

    expected_response = author_data.copy()
    expected_response.update(dict(name="test author name"))
    expected_response.update(dict(id=1))

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected_response


def test_create_author_unauthorized(client):
    """
    Test creating an author without authorization.
    """

    author_data = dict(
        name="Unauthorized Author",
    )

    response = client.post("/author/", json=author_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_create_author_with_existing_name(client, token, author):
    """
    Test creating an author with a name that already exists.
    """
    headers = {"Authorization": f"Bearer {token}"}
    author_data = dict(
        name="Sample Author",
    )
    response = client.post("/author/", json=author_data, headers=headers)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "detail": "A author with this name already exists."
    }


def test_create_author_missing_fields(client, token):
    """
    Test creating an author with missing required fields.
    """
    headers = {"Authorization": f"Bearer {token}"}
    author_data = dict(
        # Missing name
    )
    response = client.post("/author/", json=author_data, headers=headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_read_author_success(client, token, author):
    """
    Test reading an existing author successfully.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/author/{author.id}", headers=headers)
    expected_response = dict(
        id=author.id,
        name="sample author",
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


def test_read_author_not_found(client, token):
    """
    Test reading a non-existing author.
    """
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/author/999", headers=headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Author not found."}
