from fastapi import FastAPI, HTTPException

from exceptions.storage_response_exception import StorageResponseException
from task_manager import TaskManager
from exceptions.task_not_found_exception import TaskNotFound
from tasks import TaskCreateData, TaskData

app = FastAPI()


@app.get("/tasks")
def get_tasks() -> dict[int, TaskData]:
    try:
        tasks = TaskManager.get_all_tasks()
    except StorageResponseException:
        raise HTTPException(status_code=502)

    return {idx: i for idx, i in enumerate(tasks)}


@app.post("/tasks")
def create_task(task: TaskCreateData) -> TaskData:
    try:
        new_task = TaskManager.create_task(task)
    except StorageResponseException:
        raise HTTPException(status_code=502)

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_task_data: TaskCreateData) -> TaskData:
    try:
        updated_task = TaskManager.update_task(task_id, new_task_data)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    except StorageResponseException:
        raise HTTPException(status_code=502)

    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    try:
        TaskManager.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    except StorageResponseException:
        raise HTTPException(status_code=502)
