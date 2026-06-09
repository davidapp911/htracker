import datetime

import factory
from factory.alchemy import SQLAlchemyModelFactory

from backend.core.security import hash_password
from backend.models.habit import Habit, HabitCompletion
from backend.models.user import User
from tests.constants import DEFAULT_TEST_USER_PASSWORD


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    username = factory.Sequence(lambda n: f"user{n}")
    hashed_password = factory.LazyFunction(lambda: hash_password(DEFAULT_TEST_USER_PASSWORD))


class HabitFactory(BaseFactory):
    class Meta:
        model = Habit

    name = factory.Sequence(lambda n: f"habit{n}")
    frequency = "daily"
    user = factory.SubFactory(UserFactory)


class HabitCompletionFactory(BaseFactory):
    class Meta:
        model = HabitCompletion

    logged_at = factory.LazyFunction(datetime.date.today)
    habit = factory.SubFactory(HabitFactory)
