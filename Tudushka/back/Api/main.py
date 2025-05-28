from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes_task import router as task_router
from database.database import database, engine, metadata
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # запуск
    metadata.create_all(engine)
    await database.connect()
    yield
    # завершение
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
