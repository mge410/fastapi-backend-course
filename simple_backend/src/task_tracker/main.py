from fastapi import FastAPI, HTTPException

from task_manager import TaskManager
from task_not_found_exception import TaskNotFound
from tasks import TaskCreateData

app = FastAPI()


@app.get("/tasks")
def get_tasks():
    tasks = TaskManager.get_all_tasks()

    return {idx: i for idx, i in enumerate(tasks)}


@app.post("/tasks")
def create_task(task: TaskCreateData):
    new_task = TaskManager.create_task(task)

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_task_data: TaskCreateData):
    try:
        updated_task = TaskManager.update_task(task_id, new_task_data)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    try:
        TaskManager.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    pass
