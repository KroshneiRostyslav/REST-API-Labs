from uuid import UUID
from sqlalchemy.orm import Session

from app.schemas.book import BookCreate, BookStatus, BookSort
from app.repository.book_repository import BookRepository
from app.models.book import Book

class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def get_all_books(
        self,
        db: Session,
        author: str | None = None,
        status: BookStatus | None = None,
        sort: BookSort | None = None,
        limit: int | None = None,
        offset: int | None = None
    ):
        return self.repository.get_all_books(db, author, status, sort, limit, offset)

    def add_book(self, db: Session, book_data: BookCreate):
        book = Book(**book_data.model_dump())

        return self.repository.add_book(db, book)

    def get_book_by_id(self, db: Session, book_id: UUID):
        return self.repository.get_book_by_id(db, book_id)
    
    def delete_book_by_id(self, db: Session, book_id: UUID):
        return self.repository.delete_book_by_id(db, book_id)