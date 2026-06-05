import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import backend.models  # noqa: F401 — registers models with Base.metadata
from backend.api.deps import database_session
from backend.db.base import Base
from backend.main import app
from tests.constants import DEFAULT_TEST_USER_PASSWORD
from tests.factories import UserFactory


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.rollback()
        db_session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[database_session] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def create_user(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    user = UserFactory.create()
    user.password = DEFAULT_TEST_USER_PASSWORD

    yield user

    UserFactory._meta.sqlalchemy_session = None


@pytest.fixture
def auth_headers(create_user, db_session):
    from backend.core.security import create_access_token
    from backend.models.user import User

    user = db_session.query(User).filter_by(email=create_user.email).first()
    token = create_access_token(user.id)

    return {"Authorization": f"Bearer {token}"}
