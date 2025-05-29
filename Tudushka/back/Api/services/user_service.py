from database.database import database
from back.Api.models.user_models import users_table

class UserService:
    @staticmethod
    async def create_user(user: dict):
        query = users_table.insert().values(**user)
        return await database.execute(query)

    @staticmethod
    async def get_user_by_email(email: str):
        query = users_table.select().where(users_table.c.email == email)
        return await database.fetch_one(query)

    @staticmethod
    async def get_user_by_id(user_id: int):
        query = users_table.select().where(users_table.c.id == user_id)
        return await database.fetch_one(query)
