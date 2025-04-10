from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Создаем словарь для хранения Todo и переменную для генерации id
fake_db = {}
counter = 1  # Используем для генерации id

app = FastAPI()

# Модели для входных и выходных данных
class TodoCreate(BaseModel):
    title: str
    description: str

class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool

class Todo(TodoCreate):
    id: int
    completed: bool

    class Config:
        orm_mode = True

# Конечная точка для создания Todo
@app.post("/todos/", response_model=Todo)
def create_todo(todo: TodoCreate):
    global counter  # Глобальная переменная для инкремента id
    new_todo = Todo(id=counter, title=todo.title, description=todo.description, completed=False)
    fake_db[counter] = new_todo
    counter += 1  # Увеличиваем счетчик для следующего id
    return new_todo

# Конечная точка для получения Todo по ID
@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    if todo_id not in fake_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return fake_db[todo_id]

# Конечная точка для обновления Todo
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate):
    if todo_id not in fake_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    existing_todo = fake_db[todo_id]
    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.completed = todo.completed
    fake_db[todo_id] = existing_todo
    return existing_todo

# Конечная точка для удаления Todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in fake_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    del fake_db[todo_id]
    return {"message": "Todo successfully deleted"}