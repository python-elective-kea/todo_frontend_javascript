from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # CORS
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database for todos
class Todo(BaseModel):
    id: int
    title: str
    completed: bool

class TodoCreate(BaseModel):
    title: str
    completed: bool

# In-memory storage
todos_db = []
next_id = 1

@app.get("/api/todos", response_model=List[Todo])
async def get_todos():
    return todos_db

@app.post("/api/todos", response_model=Todo)
async def create_todo(todo: TodoCreate):
    global next_id
    new_todo = Todo(id=next_id, title=todo.title, completed=todo.completed)
    todos_db.append(new_todo)
    next_id += 1
    return new_todo


