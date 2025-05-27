from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from exceptions.gateway_response_exception import GatewayResponseException
from task_manager import TaskManager
from exceptions.task_not_found_exception import TaskNotFound
from task_model import TaskCreateData, TaskData

app = FastAPI()
load_dotenv()

task_manager = TaskManager()


@app.get("/tasks")
def get_tasks() -> dict[int, TaskData]:
    try:
        tasks = task_manager.get_all_tasks()
    except GatewayResponseException:
        raise HTTPException(status_code=502)

    return {idx: i for idx, i in enumerate(tasks)}


@app.post("/tasks")
def create_task(task: TaskCreateData) -> TaskData:
    try:
        new_task = task_manager.create_task(task)
    except GatewayResponseException:
        raise HTTPException(status_code=502)

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_task_data: TaskCreateData) -> TaskData:
    try:
        updated_task = task_manager.update_task(task_id, new_task_data)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    except GatewayResponseException:
        raise HTTPException(status_code=502)

    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    try:
        task_manager.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    except GatewayResponseException:
        raise HTTPException(status_code=502)
