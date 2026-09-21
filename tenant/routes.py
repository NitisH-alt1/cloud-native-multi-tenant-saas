from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.database.models import Tenant

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_tenant(
    name: str,
    slug: str,
    db: Session = Depends(get_db)
):
    existing_tenant = db.query(Tenant).filter(
        Tenant.slug == slug
    ).first()

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
        "id": tenant.id,
        "name": tenant.name,
        "slug": tenant.slug
    }


@router.get("/")
def get_tenants(
    db: Session = Depends(get_db)
):
    tenants = db.query(Tenant).all()

    return [
        {
            "id": tenant.id,
            "name": tenant.name,
            "slug": tenant.slug
        }
        for tenant in tenants
    ]
