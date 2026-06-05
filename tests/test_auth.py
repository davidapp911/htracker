import pytest

from backend.schemas.user import LoginRequest, TokenResponse, UserRead


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
    UserRead.model_validate(response.json())


@pytest.mark.auth
def test_login(create_user, client):
    response = client.post(
        "/auth/login",
        json=LoginRequest.model_validate(create_user).model_dump(),
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
    UserRead.model_validate(response.json())


@pytest.mark.auth
def test_me_without_valid_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
