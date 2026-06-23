import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_book(client):
    response = client.post(
    "/books/",
    json={
    "name": "Clean Code",
    "author": "Robert Martin",
    "description": "book",
    "year": 2008,
    "status": "available"
    }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Clean Code"
    assert "id" in data
    assert "created_at" in data

def test_get_books(client):
    response = client.get("/books/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert isinstance(data["items"], list)

def test_get_book_by_id(client):
    create = client.post(
    "/books/",
    json={
    "name": "Test",
    "author": "John",
    "description": "book",
    "year": 2020,
    "status": "available"
    }
    ).json()

    response = client.get(
        f"/books/{create['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == create["id"]

def test_get_book_not_found(client):
    response = client.get(
    "/books/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404

def test_delete_book(client):
    create = client.post(
    "/books/",
    json={
    "name": "Delete me",
    "author": "John",
    "description": "book",
    "year": 2020,
    "status": "available"
    }
    ).json()

    response = client.delete(
        f"/books/{create['id']}"
    )

    assert response.status_code == 204

def test_delete_is_idempotent(client):
    create = client.post(
    "/books/",
    json={
    "name": "Delete",
    "author": "John",
    "description": "book",
    "year": 2020,
    "status": "available"
    }
    ).json()

    book_id = create["id"]

    response1 = client.delete(
        f"/books/{book_id}"
    )

    response2 = client.delete(
        f"/books/{book_id}"
    )

    assert response1.status_code == 204
    assert response2.status_code == 204

def test_create_book_invalid_year(client):
    response = client.post(
    "/books/",
    json={
    "name": "Book",
    "author": "John",
    "description": "book",
    "year": "invalid",
    "status": "available"
    }
    )

    assert response.status_code == 422

def test_limit_offset_pagination(client):
    response = client.get(
    "/books/?limit=2&offset=0"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) <= 2
    assert data["limit"] == 2
    assert data["offset"] == 0

def test_limit_offset_next_page(client):
    first_page = client.get(
    "/books/?limit=1&offset=0"
    ).json()

    second_page = client.get(
        "/books/?limit=1&offset=1"
    ).json()

    if (
        first_page["items"]
        and second_page["items"]
    ):
        assert (
            first_page["items"][0]["id"]
            != second_page["items"][0]["id"]
        )
