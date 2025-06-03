from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from dependency import get_tasks_repository, get_tasks_service, get_request_user_id
from repository.task import TaskRepository
from schema import TaskCreateSchema, TaskSchema
from service.task import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_tasks_service)]
):
    return task_service.get_tasks()

@router.post("/", response_model=TaskSchema)
async def create_tasks(
        task: TaskCreateSchema,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)
):
    try:
        task = task_service.create_task(task, user_id)
        return task
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(
        task_id: int,
        name: str,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)
):
    try:
        updated_task = task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
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
async def delete_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)
):
    try:
        task_service.delete_task(task_id,user_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Task not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
