from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.book import BookCreate
from app.repository.book_repository import BookRepository
from app.models.book import Book

class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def get_all_books(
        self,
        db: Session,
        limit: int | None = None,
        cursor: datetime | None = None
    ):
        books = self.repository.get_all_books(db, limit, cursor)

        next_cursor = None

        if len(books) == limit:
            next_cursor = books[-1].created_at

        return {
            "items": books,
            "next_cursor": next_cursor
        }

    def add_book(self, db: Session, book_data: BookCreate):
        book = Book(**book_data.model_dump())

        return self.repository.add_book(db, book)

    def get_book_by_id(self, db: Session, book_id: UUID):
        return self.repository.get_book_by_id(db, book_id)
    
    def delete_book_by_id(self, db: Session, book_id: UUID):
        return self.repository.delete_book_by_id(db, book_id)