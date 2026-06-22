from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.exceptions import AuthenticationError, DuplicateError, NotFoundError
from backend.core.security import create_access_token, hash_password, verify_password
from backend.models.user import User
from backend.schemas.user import LoginRequest, TokenResponse, UserCreate


def register_user(db: Session, data: UserCreate) -> User:
    if db.execute(select(User).where(User.email == data.email)).scalar_one_or_none():
        raise DuplicateError("Email already in use.")

    if db.execute(select(User).where(User.username == data.username)).scalar_one_or_none():
        raise DuplicateError("Username already taken.")

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, data: LoginRequest) -> TokenResponse:
    user = db.execute(select(User).where(User.username == data.username)).scalar_one_or_none()

    if not user:
        raise NotFoundError("Username not found.")

    correct_password = verify_password(data.password, user.hashed_password)

    if not correct_password:
        raise AuthenticationError("Password does not match.")

    return TokenResponse(access_token=create_access_token(user.id))
