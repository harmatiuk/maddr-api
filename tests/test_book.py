from http import HTTPStatus


def test_successful_book_creation(client, token):
    """
    Test creating a new book successfully.
    """
    headers = {"Authorization": f"Bearer {token}"}
    book_data = dict(
        title="Test Book Title",
        author_id=1,
        publish_year=2024,
    )

    response = client.post("/book/", json=book_data, headers=headers)

    expected_response = book_data.copy()
    expected_response.update(dict(title="test book title"))
    expected_response.update(dict(id=1))

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected_response


def test_create_book_unauthorized(client):
    """
    Test creating a book without authorization.
    """

    book_data = dict(
        title="Unauthorized Book",
        author_id=1,
        publish_year=2024,
    )

    response = client.post("/book/", json=book_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_create_book_missing_fields(client, token):
    """
    Test creating a book with missing required fields.
    """
    headers = {"Authorization": f"Bearer {token}"}
    book_data = dict(
        title="Incomplete Book",
        # Missing author_id and publish_year
    )
    response = client.post("/book/", json=book_data, headers=headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_create_book_with_special_characters_in_title(client, token):
    """
    Test creating a book with special characters in the title.
    """
    headers = {"Authorization": f"Bearer {token}"}
    book_data = dict(
        title="  Special!@# Book $$ Title %%  ",
        author_id=1,
        publish_year=2024,
    )

    response = client.post("/book/", json=book_data, headers=headers)

    expected_response = book_data.copy()
    expected_response.update(dict(id=1))
    expected_response.update(dict(title="special book title"))

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected_response


def test_create_book_with_existing_title(client, token, book):
    """
    Test creating a book with a title that already exists.
    """
    headers = {"Authorization": f"Bearer {token}"}
    new_book = dict(
        author_id=1,
        title=book.title,
        publish_year=2021,
    )

    response = client.post("/book/", json=new_book, headers=headers)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "detail": "A book with this title already exists."
    }


def test_read_book_success(client, token, book):
    """
    Test reading an existing book successfully.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/book/{book.id}", headers=headers)
    expected_response = dict(
        id=book.id,
        title=book.title,
        author_id=book.author_id,
        publish_year=book.publish_year,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


def test_read_book_not_found(client, token):
    """
    Test reading a non-existing book.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/book/9999", headers=headers)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Book not found."}


def test_read_all_books_success(client, token, book):
    """
    Test reading all books successfully.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/book/?skip=0&limit=20", headers=headers)
    expected_response = [
        dict(
            id=book.id,
            title=book.title,
            author_id=book.author_id,
            publish_year=book.publish_year,
        )
    ]

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response
