from fastapi import Depends

from database import get_db_session
from repository import TaskRepository, TaskCache
from cache import get_redis_connection
from service import TaskService


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_tasks_cache_repository() -> TaskCache:
    redis_session = get_redis_connection()
    return TaskCache(redis_session)

def get_tasks_service(
    tasks_repository: TaskRepository = Depends(get_tasks_repository),
    tasks_cache_repository: TaskCache = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(
        tasks_repository=tasks_repository,
        tasks_cache_repository=tasks_cache_repository
    )