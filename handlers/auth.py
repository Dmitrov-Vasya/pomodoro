from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse

from dependency import get_auth_service
from exception import UserNotFoundException, UserNotCorrectPasswordException
from schema import UserCreateSchema
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserCreateSchema)
async def login( body: UserCreateSchema, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
       return auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)


@router.get("/login/yandex", response_class=RedirectResponse)
async def yandex_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get("/yandex")
async def yandex_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return auth_service.yandex_auth(code=code)