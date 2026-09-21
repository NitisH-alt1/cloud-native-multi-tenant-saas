from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    tenant_id: int


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
