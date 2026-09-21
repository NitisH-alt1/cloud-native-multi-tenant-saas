from fastapi import APIRouter

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.get("/")
def get_projects():
    return {
        "message": "Project management API is working"
    }


@router.post("/")
def create_project(name: str):
    return {
        "message": "Project created successfully",
        "project": {
            "name": name
        }
    }


@router.get("/{project_id}")
def get_project(project_id: int):
    return {
        "message": "Project retrieved successfully",
        "project_id": project_id
    }
