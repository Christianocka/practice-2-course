from fastapi import APIRouter, Depends, HTTPException, Query, Header
from typing import List
from back.Api.models.task_models import TaskCreateScheme, TaskScheme
from back.Api.services.task_service import TaskService
from back.Api.routes.user_routes import get_current_user_id
from jose import jwt
from back.settings import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

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
    task_dict["done"] = False
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
    updated = await TaskService.update_task(task_id, user_id, task.model_dump())
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

@router.patch(
    "/tasks/{task_id}/toggle_done"
)
async def toggle_task_done(
    task_id: int,
    user_id: int = Depends(get_current_user_id)
):
    updated = await TaskService.toggle_done(task_id, user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"status": "toggled"}

