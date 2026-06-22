from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.book import Book
from app.schemas.book import BookStatus, BookSort

class BookRepository:
    def get_all_books(
        self,
        db: Session,
        author: str | None = None,
        status: BookStatus | None = None,
        sort: BookSort | None = None,
        limit: int | None = None,
        offset: int | None = None
    ):
        query = select(Book)

        if author:
            query = query.where(Book.author == author)

        if status:
            query = query.where(Book.status == status.value)

        if sort == BookSort.by_name:
            query = query.order_by(Book.name)

        if sort == BookSort.by_year:
            query = query.order_by(Book.year)

        query = query.offset(offset).limit(limit)

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