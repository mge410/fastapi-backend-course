import json
from typing import List

from fastapi import FastAPI, HTTPException

from tasks import TaskData, TaskCreate

STORAGE_PATH = "storage.json"

app = FastAPI()


@app.get("/tasks")
def get_tasks():
    with open(STORAGE_PATH, "r") as file:
        data = json.load(file)
    tasks = [
        TaskData(id=task["id"], title=task["title"], status=task["status"])
        for task in data
    ]

    return {idx: i for idx, i in enumerate(tasks)}


@app.post("/tasks")
def create_task(task: TaskCreate):
    with open(STORAGE_PATH, "r+") as file:
        data = json.load(file)
        tasks = [
            TaskData(id=task["id"], title=task["title"], status=task["status"])
            for task in data
        ]

        task_id = get_new_task_id(tasks)
        new_task = TaskData(id=task_id, title=task.title, status=task.status)

        data.append(new_task.model_dump())

        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_task_data: TaskCreate):
    with open(STORAGE_PATH, "r+") as file:
        data = json.load(file)
        tasks = [
            TaskData(id=task["id"], title=task["title"], status=task["status"])
            for task in data
        ]

        task_index = find_task_index_by_id(task_id, tasks)
        tasks[task_index].title = new_task_data.title
        tasks[task_index].status = new_task_data.status

        file.seek(0)
        json.dump([task.model_dump() for task in tasks], file, indent=2)
        file.truncate()

    return tasks[task_index]


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with open(STORAGE_PATH, "r+") as file:
        data = json.load(file)
        tasks = [
            TaskData(id=task["id"], title=task["title"], status=task["status"])
            for task in data
        ]

        task_index = find_task_index_by_id(task_id, tasks)
        tasks.pop(task_index)

        file.seek(0)
        json.dump([task.model_dump() for task in tasks], file, indent=2)
        file.truncate()

    pass


def get_new_task_id(tasks: List[TaskData]) -> int:
    if len(tasks) > 0:
        return tasks[-1].id + 1
    return 1


def find_task_index_by_id(task_id: int, tasks: List[TaskData]) -> int:
    try:
        return [t.id for t in tasks].index(task_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")
