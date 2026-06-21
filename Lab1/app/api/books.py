from fastapi import APIRouter, HTTPException
from uuid import UUID

from app.services.book_service import BookServices
from app.schemas.book import BookCreate, BookStatus, BookResponse, BookSort
from app.repository.book_repository import BookRepository

book_router = APIRouter(prefix="/books")
repository = BookRepository()
service = BookServices(repository)

@book_router.get(
    "/",
    response_model=list[BookResponse]
)
async def get_books(
    author: str | None = None,
    status: BookStatus | None = None,
    sort: BookSort | None = None
):
    return await service.get_all_books(author, status, sort)

@book_router.get(
    "/{book_id}",
    response_model=BookResponse
)
async def get_book(book_id: UUID):
    book = await service.get_book_by_id(book_id)

    if book is None:
        raise HTTPException(
            404,
            "Book not found"
        )
    
    return book

@book_router.post(
    "/",
    response_model=BookResponse, 
    status_code=201
)
async def add_book(book: BookCreate):
    return await service.add_book(book)

@book_router.delete("/{book_id}", status_code=204)
async def delete_book_by_id(book_id: UUID):
    await service.delete_book_by_id(book_id)