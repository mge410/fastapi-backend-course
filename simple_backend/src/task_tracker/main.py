from fastapi import FastAPI, HTTPException

from tasks import TaskData, TaskStatus, TaskCreate

app = FastAPI()

tasks = [
    TaskData(id=1, title="Task new", status=TaskStatus.NEW),
    TaskData(id=2, title="Task running", status=TaskStatus.RUNNING),
    TaskData(id=3, title="Task done", status=TaskStatus.DONE),
]


@app.get("/tasks")
def get_tasks():
    return {idx: i for idx, i in enumerate(tasks)}


@app.post("/tasks")
def create_task(task: TaskCreate):
    global tasks
    task_id = get_new_task_id()
    tasks.append(TaskData(id=task_id, title=task.title, status=task.status))
    return tasks[-1]


@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_task_data: TaskCreate):
    global tasks
    task_index = find_task_index_by_id(task_id)

    tasks[task_index].title = new_task_data.title
    tasks[task_index].status = new_task_data.status
    return tasks[task_index]


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    global tasks
    task_index = find_task_index_by_id(task_id)
    tasks.pop(task_index)
    pass


def get_new_task_id():
    if len(tasks) > 0:
        return tasks[-1].id + 1
    return 1


def find_task_index_by_id(task_id: int) -> int:
    try:
        return [t.id for t in tasks].index(task_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")
