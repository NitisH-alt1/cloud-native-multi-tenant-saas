from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from auth.schemas import UserRegister, UserLogin, TokenResponse
from auth.security import hash_password, verify_password, create_access_token
from auth.service import get_user_by_username, create_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_username(
        db,
        user.username,
        user.tenant_id
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists for this tenant"
        )

    password_hash = hash_password(user.password)

    new_user = create_user(
        db=db,
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        tenant_id=user.tenant_id
    )

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "username": new_user.username,
        "tenant_id": new_user.tenant_id
    }


@router.post("/login", response_model=TokenResponse)
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_username(
        db,
        user.username,
        user.tenant_id
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={
            "user_id": existing_user.id,
            "tenant_id": existing_user.tenant_id,
            "role": existing_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
