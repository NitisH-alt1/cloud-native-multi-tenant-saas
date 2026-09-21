from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    email: str = Field(
        ...,
        min_length=5,
        max_length=150
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )

    tenant_id: int = Field(
        ...,
        gt=0
    )


class UserLogin(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )

    tenant_id: int = Field(
        ...,
        gt=0
    )


class AdminUserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    email: str = Field(
        ...,
        min_length=5,
        max_length=150
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
