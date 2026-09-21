from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Task, Project
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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tasks = (
        db.query(Task)
        .join(Project)
        .filter(Project.tenant_id == current_user.tenant_id)
        .all()
    )

    return {
        "tenant_id": current_user.tenant_id,
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "project_id": task.project_id
            }
            for task in tasks
        ]
    }


@router.post("/")
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == task_data.project_id,
            Project.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if project is None:
        return {
            "message": "Project not found for this tenant"
        }

    task = Task(
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        status="pending"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "message": "Task created successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "project_id": task.project_id,
            "tenant_id": current_user.tenant_id
        }
    }


@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = (
        db.query(Task)
        .join(Project)
        .filter(
            Task.id == task_id,
            Project.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if task is None:
        return {
            "message": "Task not found"
        }

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "project_id": task.project_id,
        "tenant_id": current_user.tenant_id
    }


@router.put("/{task_id}/status")
def update_task_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = (
        db.query(Task)
        .join(Project)
        .filter(
            Task.id == task_id,
            Project.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if task is None:
        return {
            "message": "Task not found"
        }

    task.status = status

    db.commit()
    db.refresh(task)

    return {
        "message": "Task status updated successfully",
        "task_id": task.id,
        "status": task.status,
        "tenant_id": current_user.tenant_id
    }
