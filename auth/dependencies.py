from fastapi import Depends, Header, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import User
from auth.security import decode_access_token


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ", 1)[1]

    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")
    tenant_id = payload.get("tenant_id")

    if user_id is None or tenant_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.tenant_id == tenant_id
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
