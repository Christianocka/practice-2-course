from fastapi import APIRouter, HTTPException
from typing import List
from models import TaskScheme
from base import tasks

router = APIRouter()

# Получение всех задач
@router.get("/tasks", response_model=List[TaskScheme])
async def list_tasks():
    return tasks

# Добавление задачи
@router.post("/tasks")
async def create_task(new_task: TaskScheme):
    for task in tasks:
        if task.index == new_task.index:
            raise HTTPException(status_code=400, detail="Задача с таким индексом уже существует")
    tasks.append(new_task)
    return {"message": f"Задача добавлена: {new_task.task}"}

# Обновление состояния (выполнено/не выполнено)
@router.put("/toggle/{index}")
async def toggle_task(index: int):
    for task in tasks:
        if task.index == index:
            task.done = not task.done
            status = "выполнена" if task.done else "не выполнена"
            return {"message": f"Задача изменила свой статус: {status}"}
    raise HTTPException(status_code=404, detail="Задача не найдена")


# Удаление задачи
@router.delete("/delete/{index}")
async def delete_task(index: int):
    for task in tasks:
        if task.index == index:
            tasks.remove(task)
            return {"message": f"Задача {index} удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")
