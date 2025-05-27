import json
import os
from typing import List

import requests
from dotenv import load_dotenv

from exceptions.storage_response_exception import (
    StorageResponseException,
)
from exceptions.task_not_found_exception import TaskNotFound
from tasks import TaskData, TaskCreateData

load_dotenv()


class TaskManager:
    @classmethod
    def get_all_tasks(cls) -> List[TaskData]:
        url = cls.__get_storage_url()
        response = requests.get(
            url, json=None, headers=cls.__get_storage_request_headers()
        )
        cls.__check_response_status(response.status_code)

        data = json.loads(response.text)["record"]["tasks"]

        return [
            TaskData(id=task["id"], title=task["title"], status=task["status"])
            for task in data
        ]

    @classmethod
    def create_task(cls, new_task_data: TaskCreateData) -> TaskData:
        tasks = cls.get_all_tasks()

        task_id = cls.__get_new_task_id(tasks)
        new_task = TaskData(
            id=task_id, title=new_task_data.title, status=new_task_data.status
        )

        tasks.append(new_task)
        url = cls.__get_storage_url()
        response = requests.put(
            url,
            json=cls.__format_request_body(tasks),
            headers=cls.__get_storage_request_headers(),
        )
        cls.__check_response_status(response.status_code)

        return new_task

    @classmethod
    def update_task(cls, task_id: int, new_task_data: TaskCreateData) -> TaskData:
        tasks = TaskManager.get_all_tasks()
        task_index = cls.__find_task_index_by_id(task_id, tasks)

        tasks[task_index].title = new_task_data.title
        tasks[task_index].status = new_task_data.status

        url = cls.__get_storage_url()
        response = requests.put(
            url,
            json=cls.__format_request_body(tasks),
            headers=cls.__get_storage_request_headers(),
        )
        cls.__check_response_status(response.status_code)

        return tasks[task_index]

    @classmethod
    def delete_task(cls, task_id: int) -> None:
        tasks = cls.get_all_tasks()
        task_index = cls.__find_task_index_by_id(task_id, tasks)

        tasks.pop(task_index)

        url = cls.__get_storage_url()
        response = requests.put(
            url,
            json=cls.__format_request_body(tasks),
            headers=cls.__get_storage_request_headers(),
        )
        cls.__check_response_status(response.status_code)

    @classmethod
    def __format_request_body(cls, tasks) -> dict:
        return {"tasks": [task.model_dump() for task in tasks] if tasks else []}

    @classmethod
    def __find_task_index_by_id(cls, task_id: int, tasks: List[TaskData]) -> int:
        try:
            return [t.id for t in tasks].index(task_id)
        except ValueError:
            raise TaskNotFound

    @classmethod
    def __get_new_task_id(cls, tasks: List[TaskData]) -> int:
        if len(tasks) > 0:
            return tasks[-1].id + 1
        return 1

    @classmethod
    def __get_storage_url(cls) -> str:
        return f"https://api.jsonbin.io/v3/b/{os.getenv('JSON_BIN_ID')}"

    @classmethod
    def __get_storage_request_headers(cls) -> dict:
        return {
            "Content-Type": "application/json",
            "X-Master-Key": os.getenv("JSON_BIN_IO_KEY"),
        }

    @classmethod
    def __check_response_status(cls, status: int):
        if status != 200:
            raise StorageResponseException
