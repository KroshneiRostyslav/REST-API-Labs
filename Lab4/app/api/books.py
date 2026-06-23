from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from app.dependencies import get_book_service
from app.schemas.book import (
    BookCreate,
    BookResponse,
    BookPage
)
from app.services.book_service import BookService

book_router = APIRouter(prefix="/books")


@book_router.get(
    "/",
    response_model=BookPage
)
async def get_all_books(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: BookService = Depends(get_book_service)
):
    return await service.get_all_books(
        limit,
        offset
    )


@book_router.get(
    "/{book_id}",
    response_model=BookResponse
)
async def get_book(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    book = await service.get_book_by_id(book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


@book_router.post(
    "/",
    response_model=BookResponse,
    status_code=201
)
async def add_book(
    book: BookCreate,
    service: BookService = Depends(get_book_service)
):
    return await service.add_book(book)


@book_router.delete(
    "/{book_id}",
    status_code=204
)
async def delete_book_by_id(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    await service.delete_book_by_id(book_id)