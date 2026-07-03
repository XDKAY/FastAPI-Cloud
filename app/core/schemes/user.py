from typing import Annotated, Self
from string import punctuation
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    SecretStr,
    field_validator,
    ConfigDict
)

from app.core.security.hashing import hash_password


class UserCreateScheme(BaseModel):
    username: Annotated[str, Field(..., min_length=3, max_length=20)]
    email: EmailStr
    password: Annotated[SecretStr, Field(..., min_length=12, max_length=25)]

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str) -> str:
        if not username.isalnum():
            raise ValueError("Username must be alphanumeric")
        return username


    @field_validator("password")
    @classmethod
    def validate_password(cls, password: SecretStr) -> SecretStr:
        value = password.get_secret_value()

        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        if not any(char in punctuation for char in value):
            raise ValueError("Password must contain at least one punctuation character")

        return password


class UserDTO(BaseModel):
    username: str
    email: str
    hashed_password: str

    @classmethod
    def from_create_scheme(cls, user: UserCreateScheme) -> Self:
        return UserDTO(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password.get_secret_value())
        )



class UserPrivateScheme(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    username: str
    email: str