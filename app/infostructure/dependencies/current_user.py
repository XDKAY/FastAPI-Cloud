from typing import Annotated
from fastapi import Depends

from app.core.schemes.user import UserPrivateScheme
from app.infostructure.authentication.authentication import get_current_user


CurrentUserDep = Annotated[UserPrivateScheme, Depends(get_current_user)]