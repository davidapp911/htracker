import os

import httpx
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from tests.constants import APP_LOCAL_URL

API_LOCAL_URL = "http://localhost:8000"

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


@pytest.fixture
def authenticated_page(page, create_user):
    response = httpx.post(
        f"{API_LOCAL_URL}/auth/login",
        json={"username": create_user.username, "password": create_user.password},
    )
    token = response.json()["access_token"]
    page.add_init_script(f"localStorage.setItem('token', '{token}')")
    yield page
