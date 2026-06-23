from fastapi import APIRouter, HTTPException, Depends, Query
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.book_service import BookService
from app.schemas.book import BookCreate, BookResponse, BookPage
from app.repository.book_repository import BookRepository
from app.database import get_db

book_router = APIRouter(prefix="/books")
repository = BookRepository()
service = BookService(repository)

@book_router.get(
    "/",
    response_model=BookPage
)
async def get_all_books(
    db: Session = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=100),
    cursor: datetime | None = None
):
    return service.get_all_books(db, limit, cursor)

@book_router.get(
    "/{book_id}",
    response_model=BookResponse
)
async def get_book(
    book_id: UUID,
    db: Session = Depends(get_db)
):
    book = service.get_book_by_id(db, book_id)

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
async def add_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):
    return service.add_book(db, book)

@book_router.delete("/{book_id}", status_code=204)
async def delete_book_by_id(
    book_id: UUID,
    db: Session = Depends(get_db)
):
    service.delete_book_by_id(db, book_id)
    return