from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int


@router.get("/")
def get_tasks(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Task management API is working",
        "tenant_id": current_user.tenant_id,
        "user_id": current_user.id
    }


@router.post("/")
def create_task(
    task: TaskCreate,
    current_user=Depends(get_current_user)
):
    return {
        "message": "Task created successfully",
        "task": {
            "title": task.title,
            "description": task.description,
            "project_id": task.project_id,
            "tenant_id": current_user.tenant_id
        }
    }


@router.get("/{task_id}")
def get_task(
    task_id: int,
    current_user=Depends(get_current_user)
):
    return {
        "message": "Task retrieved successfully",
        "task_id": task_id,
        "tenant_id": current_user.tenant_id
    }


@router.put("/{task_id}/status")
def update_task_status(
    task_id: int,
    status: str,
    current_user=Depends(get_current_user)
):
    return {
        "message": "Task status updated successfully",
        "task_id": task_id,
        "status": status,
        "tenant_id": current_user.tenant_id
    }
