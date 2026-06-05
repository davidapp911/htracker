import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    username: str
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    username: str
    created_at: datetime.datetime


class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
