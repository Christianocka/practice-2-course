from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class ToDo(BaseModel):
    index: int
    task: str
    done: bool = False

tasks: List[ToDo] = []

# Получение всех задач
@app.get("/tasks", response_model=List[ToDo])
async def list_tasks():
    return tasks

# Добавление задачи
@app.post("/add", response_model=ToDo)
async def create_task(item: ToDo):
    tasks.append(item)
    return item

# Обновление состояния (выполнено/не выполнено)
@app.put("/toggle/{index}", response_model=ToDo)
async def toggle_task(index: int):
    for task in tasks:
        if task.index == index:
            task.done = not task.done
            return task

# Удаление задачи
@app.delete("/delete/{index}")
async def delete_task(index: int):
    for task in tasks:
        if task.index == index:
            tasks.remove(task)
            return {"message": f"Задача {index} удалена"}
