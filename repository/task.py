from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from models import Tasks, Categories
from schema import TaskCreateSchema
from schema.tasks import TaskSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self):
        with self.db_session() as session:
            task = session.execute(select(Tasks)).scalars().all()
        return task

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            task = session.execute(select(Tasks).where(Tasks.id == task_id)).scalar_one_or_none()
        return task


    def get_user_task(self, user_id: int, task_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id and Tasks.user_id ==user_id)
        with self.db_session() as session:
            task = session.execute(query).scalar_one_or_none()
        return task


    def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id
        )
        try:
            with self.db_session() as session:
                session.add(task_model)
                session.commit()
                return task_model.id
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Integrity error: {e}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error in create_task: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def update_task_name(self, task_id: int, name: str) -> TaskSchema | None:
        with self.db_session() as session:
            try:
                session.query(Tasks).filter(Tasks.id == task_id).update({"name": name})
                session.commit()
                updated_task = session.query(Tasks).get(task_id)
                if updated_task is None:
                    raise NoResultFound(f"Task not found")
                return TaskSchema.from_orm(updated_task)
            except NoResultFound:
                raise
            except SQLAlchemyError as e:
                session.rollback()
                raise

    def delete_task(self, task_id: int, user_id: int) -> Tasks | None:
        with self.db_session() as session:
            session.execute(delete(Tasks).where(Tasks.id == task_id and Tasks.user_id == user_id))
            session.commit()

    def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Tasks.category_id == category_name)
        with self.db_session() as session:
            task: list[Tasks] = session.execute(query).scalars().all()
            return task



