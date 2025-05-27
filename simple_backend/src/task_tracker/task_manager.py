import json
from typing import List

from task_not_found_exception import TaskNotFound
from tasks import TaskData, TaskCreateData


class TaskManager:
    STORAGE_PATH = "storage.json"

    @classmethod
    def get_all_tasks(cls) -> List[TaskData]:
        with open(cls.STORAGE_PATH, "r") as file:
            data = json.load(file)
        return [
            TaskData(id=task["id"], title=task["title"], status=task["status"])
            for task in data
        ]

    @classmethod
    def create_task(cls, new_task_data: TaskCreateData) -> TaskData:
        with open(cls.STORAGE_PATH, "r+") as file:
            data = json.load(file)
            tasks = [
                TaskData(id=task["id"], title=task["title"], status=task["status"])
                for task in data
            ]

            task_id = cls.__get_new_task_id(tasks)
            new_task = TaskData(
                id=task_id, title=new_task_data.title, status=new_task_data.status
            )

            data.append(new_task.model_dump())

            file.seek(0)
            json.dump(data, file, indent=2)
            file.truncate()

        return new_task

    @classmethod
    def update_task(cls, task_id: int, new_task_data: TaskCreateData) -> TaskData:
        task_index = cls.__find_task_index_by_id(task_id)

        with open(cls.STORAGE_PATH, "r+") as file:
            data = json.load(file)
            tasks = [
                TaskData(id=task["id"], title=task["title"], status=task["status"])
                for task in data
            ]

            tasks[task_index].title = new_task_data.title
            tasks[task_index].status = new_task_data.status

            file.seek(0)
            json.dump([task.model_dump() for task in tasks], file, indent=2)
            file.truncate()

        return tasks[task_index]

    @classmethod
    def delete_task(cls, task_id: int) -> None:
        task_index = cls.__find_task_index_by_id(task_id)

        with open(cls.STORAGE_PATH, "r+") as file:
            data = json.load(file)
            tasks = [
                TaskData(id=task["id"], title=task["title"], status=task["status"])
                for task in data
            ]

            tasks.pop(task_index)

            file.seek(0)
            json.dump([task.model_dump() for task in tasks], file, indent=2)
            file.truncate()

    @classmethod
    def __find_task_index_by_id(cls, task_id: int) -> int:
        tasks = TaskManager.get_all_tasks()
        try:
            return [t.id for t in tasks].index(task_id)
        except ValueError:
            raise TaskNotFound

    @classmethod
    def __get_new_task_id(cls, tasks: List[TaskData]) -> int:
        if len(tasks) > 0:
            return tasks[-1].id + 1
        return 1
