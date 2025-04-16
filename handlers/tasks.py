from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from dependency import get_tasks_repository, get_tasks_service
from repository.task import TaskRepository
from repository.cache_tasks import TaskCache
from schema.tasks import TaskSchema
from service.task import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_tasks_service)]
):
    return task_service.get_tasks()

@router.post("/", response_model=TaskSchema)
async def create_tasks(task: TaskSchema, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    try:
        task_id = task_repository.create_task(task)
        task.id = task_id
        return task
    except HTTPException as e: # перехватывает HTTPException из create_task
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(task_id: int, name: str, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    try:
        updated_task = task_repository.update_task_name(task_id, name)
        return updated_task
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Task not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error in update_task: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{task_id}")
async def delete_task(task_id: int, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    try:
        task_repository.delete_task(task_id)
        return {"message": "Task deleted"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Task not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
