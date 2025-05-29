import os
from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tasksdb")

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))
metadata = MetaData()
