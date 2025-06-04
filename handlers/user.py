from typing import Annotated

from fastapi import APIRouter, Depends

from dependency import get_user_service
from schema import UserCreateSchema
from service import UserService

router = APIRouter(prefix="/user", tags=["user"])





@router.post('', response_model=UserCreateSchema)
def create_user(body: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.create_user(body.username, body.password)