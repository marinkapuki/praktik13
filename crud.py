from sqlalchemy import select
from .database import TodoDB

async def create_todo(db: AsyncSession, todo_data: dict):
    new_todo = TodoDB(**todo_data)
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo

async def get_todo(db: AsyncSession, todo_id: int):
    result = await db.execute(select(TodoDB).where(TodoDB.id == todo_id))
    return result.scalar_one_or_none()

async def update_todo(db: AsyncSession, todo_id: int, update_data: dict):
    todo = await get_todo(db, todo_id)
    if not todo:
        return None
    for key, value in update_data.items():
        setattr(todo, key, value)
    await db.commit()
    return todo

async def delete_todo(db: AsyncSession, todo_id: int):
    todo = await get_todo(db, todo_id)
    if not todo:
        return False
    await db.delete(todo)
    await db.commit()
    return True
