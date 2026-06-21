import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_book(client):
    response = client.post("/books/", json={
        "name": "Clean Code",
        "author": "Robert Martin",
        "description": "book",
        "year": 2008,
        "status": "available"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Clean Code"
    assert "id" in data

def test_get_books(client):
    response = client.get("/books/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book_by_id(client):
    create = client.post("/books/", json={
        "name": "Test",
        "author": "John",
        "description": "book",
        "year": 2020,
        "status": "available"
    }).json()

    book_id = create["id"]

    response = client.get(f"/books/{book_id}")

    assert response.status_code == 200
    assert response.json()["id"] == book_id

def test_get_book_not_found(client):
    response = client.get("/books/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404

def test_delete_book(client):
    create = client.post("/books/", json={
        "name": "Delete me",
        "author": "John",
        "description": "book",
        "year": 2020,
        "status": "available"
    }).json()

    book_id = create["id"]

    response = client.delete(f"/books/{book_id}")

    assert response.status_code == 204  

def test_filter_by_author(client):
    client.post("/books/", json={
        "name": "A",
        "author": "John",
        "description": "book",
        "year": 2020,
        "status": "available"
    })

    response = client.get("/books/?author=John")

    data = response.json()
    assert all(b["author"] == "John" for b in data)

def test_filter_by_status(client):
    response = client.get("/books/?status=available")

    data = response.json()
    assert all(b["status"] == "available" for b in data)

def test_sort_by_year(client):
    client.post("/books/", json={
        "name": "A",
        "author": "John",
        "description": "book",
        "year": 2005,
        "status": "available"
    })

    client.post("/books/", json={
        "name": "B",
        "author": "John",
        "description": "book",
        "year": 2010,
        "status": "available"
    })

    response = client.get("/books/?sort=year")

    years = [b["year"] for b in response.json()]
    assert years == sorted(years)

