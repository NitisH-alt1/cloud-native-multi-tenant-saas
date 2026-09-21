from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Tenant

from auth.schemas import UserRegister, UserLogin, TokenResponse
from auth.security import (
    hash_password,
    verify_password,
    create_access_token
)
from auth.service import (
    get_user_by_username,
    get_user_by_email,
    create_user
)
from auth.dependencies import get_current_user, require_role


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == user.tenant_id)
        .first()
    )

    if tenant is None:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

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

    existing_email = get_user_by_email(
        db,
        user.email,
        user.tenant_id
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists for this tenant"
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
        "tenant_id": new_user.tenant_id,
        "role": new_user.role
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


@router.get("/me")
def get_current_user_profile(
    current_user=Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "tenant_id": current_user.tenant_id,
        "role": current_user.role
    }


@router.post("/users")
def create_tenant_user(
    user: UserRegister,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Cannot create users for another tenant"
        )

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

    existing_email = get_user_by_email(
        db,
        user.email,
        user.tenant_id
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists for this tenant"
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
        "message": "User created successfully",
        "user_id": new_user.id,
        "username": new_user.username,
        "tenant_id": new_user.tenant_id,
        "role": new_user.role
    }
