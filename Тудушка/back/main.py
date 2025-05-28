from fastapi import FastAPI
from routes_task import router as task_router
import uvicorn

app = FastAPI()
app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
