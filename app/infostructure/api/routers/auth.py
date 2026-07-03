from typing import Annotated, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Response, Depends, Cookie, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.schemes.user import UserCreateScheme, UserPrivateScheme
from app.core.schemes.token import TokenScheme
from app.core.security.token import generate_token, decode_token

from app.infostructure.dependencies.services import UserServiceDep
from app.infostructure.authentication.authentication import authenticate_user


router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserPrivateScheme, status_code=status.HTTP_201_CREATED)
async def register(user_create_scheme: UserCreateScheme, user_service: UserServiceDep):
    existing_user = await user_service.get_existing_user(
        username=user_create_scheme.username,
        email=user_create_scheme.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that name or email already exists"
        )

    user: UserPrivateScheme = await user_service.create_user(user_create_scheme)

    return user


@router.post("/login", response_model=TokenScheme)
async def token(
    response: Response,
    user_service: UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
        user_service=user_service
    )

    access_token = generate_token(user.id, token_type="access")
    refresh_token = generate_token(user.id, token_type="refresh")

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=True,
    )

    return TokenScheme(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenScheme)
async def refresh(user_service: UserServiceDep, refresh_token: Optional[str] = Cookie(default=None)):

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )

    payload = decode_token(refresh_token)

    user_id = payload.get("sub")

    access_token = generate_token(user_id, token_type="access")

    return TokenScheme(
        token=access_token,
        type="bearer"
    )

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Successfully logged out"}

