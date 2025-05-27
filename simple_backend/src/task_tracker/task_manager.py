import json
from typing import List

from exceptions.task_not_found_exception import TaskNotFound
from gateways.CloudFlareHttpClient import CloudFlareHttpClient
from gateways.StorageHttpClient import StorageHttpClient, StorageHttpMethods
from task_model import TaskData, TaskCreateData


class TaskManager:
    def __init__(self):
        self.storage_client = StorageHttpClient()
        self.ai_client = CloudFlareHttpClient()

    def get_all_tasks(self) -> List[TaskData]:
        response = self.storage_client.send_request(StorageHttpMethods.GET.value)
        data = json.loads(response.text)["record"]["tasks"]

        return [
            TaskData(id=task["id"], title=task["title"], status=task["status"])
            for task in data
        ]

    def create_task(self, new_task_data: TaskCreateData) -> TaskData:
        tasks = self.get_all_tasks()
        task_id = self.__get_new_task_id(tasks)
        new_task = TaskData(
            id=task_id, title=new_task_data.title, status=new_task_data.status
        )

        tasks.append(new_task)
        self.storage_client.send_request(StorageHttpMethods.PUT.value, self.storage_client.format_request_body(tasks))

        return new_task

    def update_task(self, task_id: int, new_task_data: TaskCreateData) -> TaskData:
        tasks = self.get_all_tasks()
        task_index = self.__find_task_index_by_id(task_id, tasks)

        tasks[task_index].title = new_task_data.title
        tasks[task_index].status = new_task_data.status

        self.storage_client.send_request(StorageHttpMethods.PUT.value, self.storage_client.format_request_body(tasks))

        return tasks[task_index]

    def delete_task(self, task_id: int) -> None:
        tasks = self.get_all_tasks()
        task_index = self.__find_task_index_by_id(task_id, tasks)

        tasks.pop(task_index)
        self.storage_client.send_request(StorageHttpMethods.PUT.value, self.storage_client.format_request_body(tasks))

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
