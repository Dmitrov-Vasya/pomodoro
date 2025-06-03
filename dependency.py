from fastapi import Depends, security, HTTPException
from fastapi.params import Security

from database import get_db_session
from exception import TokenExpired, TokenNotCorrect
from repository import TaskRepository, TaskCache, UserRepository
from cache import get_redis_connection
from service import TaskService
from service.auth import AuthService
from service.user import UserService
from settings import Settings


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_tasks_cache_repository() -> TaskCache:
    redis_session = get_redis_connection()
    return TaskCache(redis_session)

def get_tasks_service(
    task_repository: TaskRepository = Depends(get_tasks_repository),
    tasks_cache_repository: TaskCache = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        tasks_cache_repository=tasks_cache_repository
    )

def get_user_repository() -> UserRepository:
    db_session = get_db_session()
    return UserRepository(db_session=db_session)


def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings())

def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotCorrect as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id