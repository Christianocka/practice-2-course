from fastapi import APIRouter, HTTPException
from typing import List
from back.Api.models import TaskScheme, tasks_table
from database.database import database

router = APIRouter()

@router.get("/tasks", response_model=List[TaskScheme])
async def list_tasks():
    query = tasks_table.select()
    return await database.fetch_all(query)

@router.post("/tasks")
async def create_task(new_task: TaskScheme):
    query = tasks_table.select().where(tasks_table.c.id == new_task.id)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Задача с таким id уже существует")
    insert_query = tasks_table.insert().values(
        id=new_task.id,
        task=new_task.task,
        done=new_task.done
    )
    await database.execute(insert_query)
    return {"message": "Задача добавлена"}

@router.put("/toggle/{id}")
async def toggle_task(id: int):
    query = tasks_table.select().where(tasks_table.c.id == id)
    task = await database.fetch_one(query)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    new_done_status = not task["done"]
    update_query = tasks_table.update().where(tasks_table.c.id == id).values(done=new_done_status)
    await database.execute(update_query)

    status = "выполнена" if new_done_status else "не выполнена"
    return {"message": f"Задача изменила свой статус: {status}"}

@router.delete("/delete/{id}")
async def delete_task(id: int):
    query = tasks_table.select().where(tasks_table.c.id == id)
    task = await database.fetch_one(query)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    delete_query = tasks_table.delete().where(tasks_table.c.id == id)
    await database.execute(delete_query)
    return {"message": f"Задача {id} удалена"}
