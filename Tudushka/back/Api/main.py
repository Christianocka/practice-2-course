from fastapi import FastAPI
from contextlib import asynccontextmanager
from back.Api.routes.task_routes import router as task_router
from back.Api.routes.user_routes import router as user_router
from database.database import database, engine, metadata, DATABASE_URL
import uvicorn

print("DATABASE_URL:", repr(DATABASE_URL))
print("DATABASE_URL raw bytes:", DATABASE_URL.encode("utf-8"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # запуск
    await database.connect()
    yield
    # завершение
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(task_router, prefix="", tags=["tasks"])
app.include_router(user_router, prefix="", tags=["users"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
