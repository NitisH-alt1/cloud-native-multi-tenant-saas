from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Project
from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.get("/")
def get_projects(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    projects = (
        db.query(Project)
        .filter(Project.tenant_id == current_user.tenant_id)
        .all()
    )

    return {
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "tenant_id": project.tenant_id
            }
            for project in projects
        ]
    }


@router.post("/")
def create_project(
    name: str,
    description: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    project = Project(
        name=name,
        description=description,
        tenant_id=current_user.tenant_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "message": "Project created successfully",
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "tenant_id": project.tenant_id
        }
    }


@router.get("/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "tenant_id": project.tenant_id
    }
