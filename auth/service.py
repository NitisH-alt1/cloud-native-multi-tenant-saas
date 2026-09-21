from sqlalchemy.orm import Session

from backend.database.models import User


def get_user_by_username(
    db: Session,
    username: str,
    tenant_id: int
):
    return (
        db.query(User)
        .filter(
            User.username == username,
            User.tenant_id == tenant_id
        )
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str,
    tenant_id: int
):
    return (
        db.query(User)
        .filter(
            User.email == email,
            User.tenant_id == tenant_id
        )
        .first()
    )


def create_user(
    db: Session,
    username: str,
    email: str,
    password_hash: str,
    tenant_id: int
):
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        tenant_id=tenant_id,
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
