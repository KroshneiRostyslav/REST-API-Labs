from fastapi import Depends

from app.database import db
from app.repository.book_repository import BookRepository
from app.services.book_service import BookService

def get_book_repository():
    return BookRepository(db)


def get_book_service(
    repository: BookRepository = Depends(
        get_book_repository
    )
):
    return BookService(repository)