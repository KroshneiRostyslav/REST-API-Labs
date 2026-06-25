from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import create_access_token, create_refresh_token, verify_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or form_data.password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": form_data.username})
    refresh_token = create_refresh_token({"sub": form_data.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh(refresh_token: str):
    payload = verify_token(refresh_token, "refresh")

    new_access_token = create_access_token(
        {"sub": payload["sub"]}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }