from fastapi import APIRouter, HTTPException
from typing import List
from models import TaskScheme, tasks_table
from database.database import database

router = APIRouter()

@router.get("/tasks", response_model=List[TaskScheme])
async def list_tasks():
    query = tasks_table.select()
    return await database.fetch_all(query)

@router.post("/tasks")
async def create_task(new_task: TaskScheme):
    query = tasks_table.select().where(tasks_table.c.index == new_task.index)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Задача с таким индексом уже существует")
    
    insert_query = tasks_table.insert().values(
        index=new_task.index,
        task=new_task.task,
        done=new_task.done
    )
    await database.execute(insert_query)
    return {"message": f"Задача добавлена: {new_task.task}"}

@router.put("/toggle/{index}")
async def toggle_task(index: int):
    query = tasks_table.select().where(tasks_table.c.index == index)
    task = await database.fetch_one(query)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    new_done_status = not task["done"]
    update_query = tasks_table.update().where(tasks_table.c.index == index).values(done=new_done_status)
    await database.execute(update_query)

    status = "выполнена" if new_done_status else "не выполнена"
    return {"message": f"Задача изменила свой статус: {status}"}

@router.delete("/delete/{index}")
async def delete_task(index: int):
    query = tasks_table.select().where(tasks_table.c.index == index)
    task = await database.fetch_one(query)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    delete_query = tasks_table.delete().where(tasks_table.c.index == index)
    await database.execute(delete_query)
    return {"message": f"Задача {index} удалена"}
