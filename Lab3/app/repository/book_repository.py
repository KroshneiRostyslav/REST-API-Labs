from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.models.book import Book

class BookRepository:
    def get_all_books(
        self,
        db: Session,
        limit: int | None = None,
        cursor: datetime | None = None
    ):
        query = select(Book)

        if cursor:
            query = query.where(Book.created_at > cursor)

        query = query.order_by(Book.created_at).limit(limit)

        result = db.execute(query)

        return result.scalars().all()

    def get_book_by_id(
        self,
        db: Session,
        book_id: UUID
    ):
        result = db.execute(
            select(Book).where(Book.id == book_id)
        )

        return result.scalar_one_or_none()

    def add_book(
        self,
        db: Session,
        book: Book
    ):
        db.add(book)
        db.commit()
        db.refresh(book)

        return book

    def delete_book_by_id(
        self,
        db: Session,
        book_id: UUID
    ):
        book = self.get_book_by_id(db, book_id)

        if not book:
            return False

        db.delete(book)
        db.commit()

        return True