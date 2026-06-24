from uuid import uuid4
from datetime import datetime

from app.repository.book_repository import (
    BookRepository
)


class BookService:

    def __init__(self):
        self.repository = BookRepository()

    def get_all_books(
        self,
        limit,
        offset
    ):
        books, total = (
            self.repository.get_all_books(
                limit,
                offset
            )
        )

        return {
            "items": books,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    def add_book(
        self,
        data
    ):
        book = {
            "id": str(uuid4()),
            **data,
            "created_at":
                datetime.utcnow().isoformat()
        }

        return self.repository.add_book(book)

    def get_book_by_id(
        self,
        book_id
    ):
        return self.repository.get_book_by_id(
            book_id
        )

    def delete_book_by_id(
        self,
        book_id
    ):
        return self.repository.delete_book_by_id(
            book_id
        )