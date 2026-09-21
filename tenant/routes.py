from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Tenant

from auth.dependencies import get_current_user


router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


@router.get("/")
def get_current_tenant(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == current_user.tenant_id)
        .first()
    )

    if tenant is None:
        return {
            "message": "Tenant not found"
        }

    return {
        "id": tenant.id,
        "name": tenant.name,
        "slug": tenant.slug
    }
