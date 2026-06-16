import datetime

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import backend.models  # noqa: F401 — registers models with Base.metadata
from backend.api.deps import database_session
from backend.core.config import settings
from backend.core.security import create_access_token
from backend.db.base import Base
from backend.main import app
from backend.models.user import User
from tests.constants import DEFAULT_TEST_USER_PASSWORD
from tests.factories import HabitCompletionFactory, HabitFactory, UserFactory


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[database_session] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_headers(create_user, db_session):

    user = db_session.query(User).filter_by(email=create_user.email).first()
    token = create_access_token(user.id)

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def expired_token_headers(create_user, db_session):
    payload = {
        "sub": str(create_user.id),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(minutes=1),
    }

    return {
        "Authorization": f"Bearer {jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')}"
    }


@pytest.fixture(scope="function")
def deleted_user_headers(create_user, auth_headers, db_session):
    db_session.delete(create_user)
    db_session.commit()

    return auth_headers


@pytest.fixture(scope="function")
def user_factory(db_session):
    UserFactory._meta.sqlalchemy_session = db_session

    yield UserFactory

    UserFactory._meta.sqlalchemy_session = None


@pytest.fixture(scope="function")
def create_user(user_factory):
    user = user_factory.create()
    user.password = DEFAULT_TEST_USER_PASSWORD

    return user


@pytest.fixture(scope="function")
def habit_factory(db_session):
    HabitFactory._meta.sqlalchemy_session = db_session

    yield HabitFactory

    HabitFactory._meta.sqlalchemy_session = None


@pytest.fixture(scope="function")
def create_habit(create_user, habit_factory):
    return habit_factory.create(user=create_user)


@pytest.fixture(scope="function")
def create_multiple_habits(create_user, habit_factory):
    def _factory(n: int, user=None):
        target = user or create_user
        return [habit_factory.create(user=target) for _ in range(n)]

    yield _factory


@pytest.fixture(scope="function")
def completion_factory(db_session):
    HabitCompletionFactory._meta.sqlalchemy_session = db_session

    yield HabitCompletionFactory

    HabitCompletionFactory._meta.sqlalchemy_session = None


@pytest.fixture(scope="function")
def create_completion(create_habit, completion_factory):
    return completion_factory.create(habit=create_habit)


@pytest.fixture(scope="function")
def create_multiple_completions(completion_factory):
    def _factory(pattern: list[int], habit=None):
        return [
            completion_factory.create(
                habit=habit,
                logged_at=datetime.date.today() - datetime.timedelta(days=n),
            )
            for n in pattern
        ]

    yield _factory


@pytest.fixture(scope="function")
def create_data_for_user(
    create_user, create_multiple_habits, create_multiple_completions
):
    def _factory(habit_count, completions_patterns, user=None):
        target = user or create_user
        habits = create_multiple_habits(habit_count, user=target)

        for h, pattern in zip(habits, completions_patterns):
            create_multiple_completions(pattern, habit=h)

    yield _factory
