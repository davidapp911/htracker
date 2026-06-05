import factory
from factory.alchemy import SQLAlchemyModelFactory

from backend.core.security import hash_password
from backend.models.user import User
from tests.constants import DEFAULT_TEST_USER_PASSWORD


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    username = factory.Sequence(lambda n: f"user{n}")
    hashed_password = factory.LazyFunction(lambda: hash_password(DEFAULT_TEST_USER_PASSWORD))
