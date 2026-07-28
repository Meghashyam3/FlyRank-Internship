from fastapi import FastAPI, HTTPException, Response 
from pydantic import BaseModel, Field 

app = FastAPI()

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": True
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Practice DSA",
        "done": True
    },
]

class TaskCreate(BaseModel):
    title: str = Field (min_length=1, strip_whitespace=True)

class TaskUpdate(BaseModel):
    title: str = Field (min_length=1, strip_whitespace=True)
    done: bool

@app.get("/")
def home():
    return {"name":"Task API",
            "version":"1.0",
           }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
        
    raise HTTPException(
        status_code=404,
        detail="Task Not Found"
)

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_id = max(tasks, key=lambda task: task["id"])["id"] + 1
    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{id}")
def update_task(id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == id:
            task["title"] = task_update.title 
            task["done"] = task_update.done 
            return task
    raise HTTPException(
        status_code=404,
        detail="Task Not Found"
    )

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return Response(status_code=204)
    raise HTTPException(
        status_code=404,
        detail="Task Not Found"
    )