from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Todo API")

# In-memory database for local testing
todos_db = []
current_id = 1

class TodoItem(BaseModel):
    task: str

class TodoResponse(BaseModel):
    id: int
    task: str
    completed: bool

@app.get("/todos", response_model=List[TodoResponse])
def get_todos():
    return todos_db

@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoItem):
    global current_id
    new_todo = {"id": current_id, "task": todo.task, "completed": False}
    todos_db.append(new_todo)
    current_id += 1
    return new_todo

@app.put("/todos/{todo_id}")
def complete_todo(todo_id: int):
    for todo in todos_db:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos_db):
        if todo["id"] == todo_id:
            del todos_db[i]
            return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")