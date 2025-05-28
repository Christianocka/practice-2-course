from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

# Хранилище задач
tasks: List[Task] = []

tasks = [
    {
      "index": 1,
      "task": "string",
      "done": false
    },
    {
      "index": 2,
      "task": "string",
      "done": false
    }
] 
# Получение всех задач
@app.get("/tasks", response_model=List[Task])
async def list_tasks():
    return tasks

# Добавление задачи
@app.post("/tasks", response_model=Task)
async def create_task(new_task: Task):
    for task in tasks:
        if task.index == new_task.index:
            raise HTTPException(status_code=400, detail="Задача с таким индексом уже существует")
    tasks.append(new_task)
    return new_task

# Обновление состояния (выполнено/не выполнено)
@app.put("/toggle/{index}", response_model=Task)
async def toggle_task(index: int):
    for task in tasks:
        if task.index == index:
            task.done = not task.done
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Удаление задачи
@app.delete("/delete/{index}")
async def delete_task(index: int):
    for task in tasks:
        if task.index == index:
            tasks.remove(task)
            return {"message": f"Задача {index} удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")
