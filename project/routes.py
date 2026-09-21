from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.get("/")
def get_projects(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Project management API is working",
        "tenant_id": current_user.tenant_id,
        "user_id": current_user.id
    }


@router.post("/")
def create_project(
    name: str,
    current_user=Depends(get_current_user)
):
    return {
        "message": "Project created successfully",
        "project": {
            "name": name,
            "tenant_id": current_user.tenant_id
        }
    }


@router.get("/{project_id}")
def get_project(
    project_id: int,
    current_user=Depends(get_current_user)
):
    return {
        "message": "Project retrieved successfully",
        "project_id": project_id,
        "tenant_id": current_user.tenant_id
    }
