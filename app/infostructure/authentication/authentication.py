from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.schemes.user import UserPrivateScheme
from app.core.security.hashing import verify_password
from app.core.security.token import decode_token

from app.core.services.user import UserService
from app.infostructure.dependencies.services import UserServiceDep


scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def authenticate_user(username: str, password: str, user_service: UserService) -> UserPrivateScheme:
    user = await user_service.get_existing_user(
        username=username,
        email=""
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return user


async def get_current_user(user_service: UserServiceDep, token: str = Depends(scheme)) -> UserPrivateScheme:
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type"
        )

    user_id = UUID(payload.get("sub"))

    user = await user_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User unauthorized"
        )

    return user