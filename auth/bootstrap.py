from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Tenant

from auth.security import hash_password
from auth.service import get_user_by_username, get_user_by_email, create_user


router = APIRouter(
    prefix="/bootstrap",
    tags=["Bootstrap"]
)


class BootstrapRequest(BaseModel):
    tenant_name: str
    tenant_slug: str
    username: str
    email: str
    password: str


@router.post("/")
def bootstrap_tenant(
    request: BootstrapRequest,
    db: Session = Depends(get_db)
):
    existing_tenant = (
        db.query(Tenant)
        .filter(Tenant.slug == request.tenant_slug)
        .first()
    )

    if existing_tenant:
        raise HTTPException(
            status_code=400,
            detail="Tenant already exists"
        )

    tenant = Tenant(
        name=request.tenant_name,
        slug=request.tenant_slug
    )

    db.add(tenant)
    db.flush()

    existing_username = get_user_by_username(
        db,
        request.username,
        tenant.id
    )

    if existing_username:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = get_user_by_email(
        db,
        request.email,
        tenant.id
    )

    if existing_email:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    password_hash = hash_password(request.password)

    user = create_user(
        db=db,
        username=request.username,
        email=request.email,
        password_hash=password_hash,
        tenant_id=tenant.id
    )

    return {
        "message": "Tenant and admin user created successfully",
        "tenant": {
            "id": tenant.id,
            "name": tenant.name,
            "slug": tenant.slug
        },
        "admin": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "tenant_id": user.tenant_id
        }
    }
