from pydantic import BaseModel, Field
from sqlalchemy import Table, Column, Integer, String, Boolean
from back.database.database import metadata

tasks_table = Table(
    "tasks",
    metadata,
    Column("index", Integer, primary_key=True),
    Column("task", String(100), nullable=False),
    Column("done", Boolean, default=False),
)

class TaskScheme(BaseModel):
    index: int = Field(ge=1)
    task: str = Field(min_length=1, max_length=100)
    done: bool = False
