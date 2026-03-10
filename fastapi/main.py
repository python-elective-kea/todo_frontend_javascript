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


############################################################################







class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

## , response_model=List[Todo]
## , response_model=Todo

###############################################################################



@app.get("/api/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/api/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    for todo in todos_db:
        if todo.id == todo_id:
            if todo_update.title is not None:
                todo.title = todo_update.title
            if todo_update.completed is not None:
                todo.completed = todo_update.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    global todos_db
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            todos_db.pop(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
