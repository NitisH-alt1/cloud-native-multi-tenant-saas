from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Tenant
from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


@router.post("/")
def create_tenant(
    name: str,
    slug: str,
    db: Session = Depends(get_db)
):
    existing_tenant = (
        db.query(Tenant)
        .filter(Tenant.slug == slug)
        .first()
    )

    if existing_tenant:
        raise HTTPException(
            status_code=400,
            detail="Tenant already exists"
        )

    tenant = Tenant(
        name=name,
        slug=slug
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return {
        "message": "Tenant created successfully",
        "id": tenant.id,
        "name": tenant.name,
        "slug": tenant.slug
    }


@router.get("/")
def get_tenants(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tenants = (
        db.query(Tenant)
        .filter(Tenant.id == current_user.tenant_id)
        .all()
    )

    return [
        {
            "id": tenant.id,
            "name": tenant.name,
            "slug": tenant.slug
        }
        for tenant in tenants
    ]
