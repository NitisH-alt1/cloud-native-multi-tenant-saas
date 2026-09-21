from fastapi import APIRouter, Depends, HTTPException
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
        .join(Project, Task.project_id == Project.id)
        .filter(Project.tenant_id == current_user.tenant_id)
        .all()
    )

    return {
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
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == task.project_id,
            Project.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        status="pending"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "status": new_task.status,
            "project_id": new_task.project_id
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
        .join(Project, Task.project_id == Project.id)
        .filter(
            Task.id == task_id,
            Project.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "project_id": task.project_id
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
        .join(Project, Task.project_id == Project.id)
        .filter(
            Task.id == task_id,
            Project.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = status

    db.commit()
    db.refresh(task)

    return {
        "message": "Task status updated successfully",
        "task": {
            "id": task.id,
            "status": task.status
        }
    }
