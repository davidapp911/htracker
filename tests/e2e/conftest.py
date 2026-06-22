import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from tests.constants import APP_LOCAL_URL

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return APP_LOCAL_URL


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(os.environ["DATABASE_URL_E2E"])
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def reset_db(db_session):
    yield
    db_session.execute(text("TRUNCATE users, habits, completions RESTART IDENTITY CASCADE;"))
    db_session.commit()
