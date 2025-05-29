from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from back.Api.models.task_models import TaskCreateScheme, TaskScheme
from back.Api.services.task_service import TaskService
from back.Api.routes.user_routes import get_current_user_id

router = APIRouter()

@router.post(
    "/tasks", 
    response_model=int
)
async def create_task(
    task: TaskCreateScheme,
    user_id: int = Depends(get_current_user_id)
):
    task_dict = task.dict()
    task_dict["user_id"] = user_id
    return await TaskService.create_task(task_dict)

@router.get(
    "/tasks", 
    response_model=List[TaskScheme]
)
async def get_tasks(
    done: bool = Query(None),
    user_id: int = Depends(get_current_user_id)
):
    return await TaskService.get_tasks(user_id, done)

@router.get(
    "/tasks/{task_id}", 
    response_model=TaskScheme
)
async def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id)
):
    task = await TaskService.get_task(task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@router.put(
    "/tasks/{task_id}"
)
async def update_task(
    task_id: int,
    task: TaskCreateScheme,
    user_id: int = Depends(get_current_user_id)
):
    updated = await TaskService.update_task(task_id, user_id, task.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"status": "updated"}

@router.delete(
    "/tasks/{task_id}"
)
async def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id)
):
    deleted = await TaskService.delete_task(task_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"status": "deleted"}
