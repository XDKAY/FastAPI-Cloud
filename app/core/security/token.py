import jwt

from uuid import UUID
from typing import Mapping
from datetime import datetime, timezone, timedelta
from fastapi import status, HTTPException

from app.core.settings.settings import settings


def generate_token(user_id: UUID, token_type: str) -> str:

    """
        token_type:
            values: access/refresh
    """
    
    match (token_type):
        case "access":
            expires = datetime.now(timezone.utc) + timedelta(minutes=settings.token.access_token_expires_minutes)

        case "refresh":
            expires = datetime.now(timezone.utc) + timedelta(days=settings.token.refresh_token_expires_days)

        case _:
            raise ValueError("Invalid token type")
    
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "exp": expires
    }

    return jwt.encode(
        payload, 
        settings.token.secret.get_secret_value(), 
        algorithm=settings.token.algorithm
    )


def decode_token(token: str) -> Mapping[str, str]:
    try:
        payload = jwt.decode(
            token,
            settings.token.secret.get_secret_value(),
            algorithms=[settings.token.algorithm]
        )
        return payload

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
