from typing import Annotated
from fastapi import APIRouter, Depends, Response
from app.core.schemes.user import UserPrivateScheme
from app.infostructure.dependencies.services import UserServiceDep
from app.infostructure.dependencies.current_user import CurrentUserDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me",response_model=UserPrivateScheme)
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.delete("/")
async def delete_current_user(current_user: CurrentUserDep, user_service: UserServiceDep, response: Response):

    await user_service.delete_user(current_user.id)

    response.delete_cookie("refresh_token")

    return {"message": "The user has been successfully deleted"}
    