import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "hello123@gmail.com"


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user.get("email"),
            "password": test_user.get("password"),
        },
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    id_: str = payload.get("user_id")

    assert response.status_code == 200
    assert login_response.token_type == "bearer"
    assert id_ == test_user.get("id")


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("wrong_email", "password123", 403),
        ("hugo@gmail.com", "wrong_password", 403),
        ("wrong_email", "wrong_password", 403),
        (None, "password123", 422),
        ("hugo@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, username, password, status_code):
    response = client.post(
        "/login",
        data={
            "username": username,
            "password": password,
        },
    )
    assert response.status_code == status_code
    if response.status_code == 403:
        assert response.json().get("detail") == "Invalid Credentials"
