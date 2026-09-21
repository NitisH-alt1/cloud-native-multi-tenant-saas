from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int


@router.get("/")
def get_tasks():
    return {
        "message": "Task management API is working"
    }


@router.post("/")
def create_task(task: TaskCreate):
    return {
        "message": "Task created successfully",
        "task": {
            "title": task.title,
            "description": task.description,
            "project_id": task.project_id
        }
    }


@router.get("/{task_id}")
def get_task(task_id: int):
    return {
        "message": "Task retrieved successfully",
        "task_id": task_id
    }


@router.put("/{task_id}/status")
def update_task_status(task_id: int, status: str):
    return {
        "message": "Task status updated successfully",
        "task_id": task_id,
        "status": status
    }
