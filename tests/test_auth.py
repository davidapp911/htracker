import pytest

from backend.schemas.user import TokenResponse, UserResponse
from tests.constants import GARBAGE_TOKEN_HEADER


@pytest.mark.auth
def test_register_new_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123",
        },
    )

    assert response.status_code == 201
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()
    UserResponse.model_validate(response.json())


@pytest.mark.auth
def test_login(create_user, client):
    response = client.post(
        "/auth/login",
        json={"username": create_user.username, "password": create_user.password},
    )

    assert response.status_code == 200
    TokenResponse.model_validate(response.json())


@pytest.mark.auth
def test_register_duplicate_email(create_user, client):
    response = client.post(
        "/auth/register",
        json={
            "email": create_user.email,
            "username": "somenewusername",
            "password": "somenewpassword",
        },
    )

    assert response.status_code == 409


@pytest.mark.auth
def test_me_with_valid_token(auth_headers, client):
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    UserResponse.model_validate(response.json())


@pytest.mark.auth
def test_me_without_valid_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


@pytest.mark.auth
def test_me_with_expired_token(client, expired_token_headers):
    response = client.get("/auth/me", headers=expired_token_headers)

    assert response.status_code == 401


@pytest.mark.auth
def test_me_with_invalid_token(client):
    response = client.get("/auth/me", headers=GARBAGE_TOKEN_HEADER)

    assert response.status_code == 401


@pytest.mark.auth
def test_me_with_token_for_deleted_user(client, deleted_user_headers):
    response = client.get("/auth/me", headers=deleted_user_headers)

    assert response.status_code == 401


@pytest.mark.auth
def test_register_missing_field(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "username": "testuser"},
    )

    assert response.status_code == 422
