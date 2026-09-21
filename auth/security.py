import os

from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt


load_dotenv()


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-secret-key-change-in-production"
)

ALGORITHM = "HS256"


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict) -> str:
    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
