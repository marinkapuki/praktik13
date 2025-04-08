from fastapi import FastAPI, Depends, HTTPException, status
from .database import engine, get_db, Base, TodoDB
from .schemas import TodoCreate, TodoUpdate, TodoResponse
from .crud import create_todo, get_todo, update_todo, delete_todo

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo_endpoint(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await create_todo(db, todo.dict())

@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo_endpoint(
    todo_id: int, 
    update_data: TodoUpdate, 
    db: AsyncSession = Depends(get_db)
):
    updated_todo = await update_todo(db, todo_id, update_data.dict(exclude_unset=True))
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_endpoint(todo_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
