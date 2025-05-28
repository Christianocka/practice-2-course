from pydantic import BaseModel, Field

class TaskScheme(BaseModel):
    index: int = Field(ge=1)
    task: str = Field(min_length=1, max_length=100)
    done: bool = False
