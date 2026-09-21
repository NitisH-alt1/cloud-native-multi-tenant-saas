from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/")
def auth_status():
    return {
        "message": "Authentication API is working"
    }


@router.post("/login")
def login(username: str, password: str):
    return {
        "message": "Login endpoint is working",
        "username": username
    }
