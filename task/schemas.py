from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int


class TaskStatusUpdate(BaseModel):
    status: str
