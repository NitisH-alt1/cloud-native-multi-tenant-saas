from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Project

from auth.dependencies import get_current_user, require_role
from project.schemas import ProjectCreate, ProjectUpdate


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
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    project = Project(
        name=project_data.name,
        description=project_data.description,
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


@router.put("/{project_id}")
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
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

    project.name = project_data.name
    project.description = project_data.description

    db.commit()
    db.refresh(project)

    return {
        "message": "Project updated successfully",
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "tenant_id": project.tenant_id
        }
    }


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
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

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully",
        "project_id": project_id
    }
