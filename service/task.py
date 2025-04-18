from dataclasses import dataclass

from repository import TaskRepository, TaskCache
from schema.tasks import TaskSchema

@dataclass
class TaskService:
    task_repository: TaskRepository
    tasks_cache_repository:TaskCache

    def get_tasks(self) ->list[TaskSchema]:
        if tasks := self.tasks_cache_repository.get_tasks():
            return tasks
        else:
            result = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in result]
            self.tasks_cache_repository.set_task(tasks_schema)
            return tasks_schema