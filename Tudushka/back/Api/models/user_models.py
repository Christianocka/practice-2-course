from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from database.database import metadata

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(100), unique=True, nullable=False),
    Column("hashed_password", String(255), nullable=False),
)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
