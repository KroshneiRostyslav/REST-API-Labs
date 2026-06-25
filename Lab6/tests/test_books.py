import pytest

from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_add_book(client):
    response = client.post(
        "/books",
        json={
            "name": "Algorithms",
            "author": "J. Smith",
            "description": "Reference guide",
            "year": 2021,
            "status": "available"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Algorithms"
    assert "id" in data
    assert "created_at" in data


def test_get_books(client):
    response = client.get("/books")

    assert response.status_code == 200

    data = response.get_json()

    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data


def test_get_book(client):
    created = client.post(
        "/books",
        json={
            "name": "Networks",
            "author": "A. Brown",
            "description": "Study material",
            "year": 2020,
            "status": "available"
        }
    )

    book = created.get_json()

    response = client.get(
        f"/books/{book['id']}"
    )

    assert response.status_code == 200
    assert response.get_json()["id"] == book["id"]


def test_book_not_found(client):
    response = client.get(
        "/books/non-existing-id"
    )

    assert response.status_code == 404


def test_delete_book(client):
    created = client.post(
        "/books",
        json={
            "name": "Databases",
            "author": "M. Green",
            "description": "Textbook",
            "year": 2019,
            "status": "available"
        }
    )

    book = created.get_json()

    response = client.delete(
        f"/books/{book['id']}"
    )

    assert response.status_code == 204


def test_delete_twice(client):
    created = client.post(
        "/books",
        json={
            "name": "Systems",
            "author": "L. White",
            "description": "Course notes",
            "year": 2022,
            "status": "available"
        }
    )

    book = created.get_json()

    first = client.delete(
        f"/books/{book['id']}"
    )

    second = client.delete(
        f"/books/{book['id']}"
    )

    assert first.status_code == 204
    assert second.status_code == 204


def test_pagination(client):
    response = client.get(
        "/books?limit=2&offset=0"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["limit"] == 2
    assert data["offset"] == 0
    assert len(data["items"]) <= 2