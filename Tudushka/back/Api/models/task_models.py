from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from database.database import metadata

tasks_table = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task", String(100), nullable=False),
    Column("done", Boolean, default=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
)

class TaskScheme(BaseModel):
    id: int = Field(ge=1)
    task: str = Field(min_length=1, max_length=100)
    done: bool = False

class TaskCreateScheme(BaseModel):
    task: str = Field(min_length=1, max_length=100)
    done: bool = False
