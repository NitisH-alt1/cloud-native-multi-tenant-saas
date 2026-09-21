from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Task, Project

from auth.dependencies import get_current_user, require_role
from task.schemas import TaskCreate, TaskStatusUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


ALLOWED_TASK_STATUSES = {
    "pending",
    "in_progress",
    "completed"
}


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
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
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
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
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
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    if status_data.status not in ALLOWED_TASK_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid task status"
        )

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

    task.status = status_data.status

    db.commit()
    db.refresh(task)

    return {
        "message": "Task status updated successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "project_id": task.project_id
        }
    }
