from database.database import database
from back.Api.models.task_models import tasks_table
from typing import Optional

class TaskService:
    @staticmethod
    async def create_task(task: dict):
        query = tasks_table.insert().values(**task)
        return await database.execute(query)

    @staticmethod
    async def get_tasks(user_id: int, done: Optional[bool] = None):
        query = tasks_table.select().where(tasks_table.c.user_id == user_id)
        if done is not None:
            query = query.where(tasks_table.c.done == done)
        result = await database.fetch_all(query)
        return [dict(row) for row in result]

    @staticmethod
    async def get_task(task_id: int, user_id: int):
        query = tasks_table.select().where(
            (tasks_table.c.id == task_id) & (tasks_table.c.user_id == user_id)
        )
        return await database.fetch_one(query)

    @staticmethod
    async def update_task(task_id: int, user_id: int, values: dict):
        query = (
            tasks_table.update()
            .where((tasks_table.c.id == task_id) & (tasks_table.c.user_id == user_id))
            .values(**values)
        )
        return await database.execute(query)

    @staticmethod
    async def delete_task(task_id: int, user_id: int):
        query = tasks_table.delete().where(
            (tasks_table.c.id == task_id) & (tasks_table.c.user_id == user_id)
        )
        return await database.execute(query)

    @staticmethod
    async def toggle_done(task_id: int, user_id: int):
        # Получаем текущий статус задачи
        query = tasks_table.select().where(
            (tasks_table.c.id == task_id) & (tasks_table.c.user_id == user_id)
        )
        task = await database.fetch_one(query)
        if not task:
            return None

        new_done = not task["done"]
        update_query = (
            tasks_table.update()
            .where((tasks_table.c.id == task_id) & (tasks_table.c.user_id == user_id))
            .values(done=new_done)
        )
        await database.execute(update_query)
        return True
