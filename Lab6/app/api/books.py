from fastapi import (
    APIRouter,
    Depends,
    Query,
    HTTPException
)
from fastapi.security import (
    OAuth2PasswordBearer
)

from app.dependencies import (
    get_book_service
)
from app.auth import verify_token

from app.schemas.book import (
    BookCreate,
    BookResponse,
    BookPage
)

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)

service = get_book_service()


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    return verify_token(
        token,
        "access"
    )


@router.get(
    "/",
    response_model=BookPage
)
def get_books(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    user=Depends(get_current_user)
):
    books = service.get_all_books(
        limit,
        offset
    )

    return {
        "items": books,
        "total": len(books),
        "limit": limit,
        "offset": offset
    }


@router.post(
    "/",
    response_model=BookResponse,
    status_code=201
)
def create_book(
    data: BookCreate,
    user=Depends(get_current_user)
):
    return service.add_book(
        data.model_dump()
    )


@router.get(
    "/{book_id}",
    response_model=BookResponse
)
def get_book(
    book_id: str,
    user=Depends(get_current_user)
):
    book = service.get_book_by_id(
        book_id
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


@router.delete(
    "/{book_id}",
    status_code=204
)
def delete_book(
    book_id: str,
    user=Depends(get_current_user)
):
    service.delete_book_by_id(
        book_id
    )