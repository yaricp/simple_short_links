from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.user import User

from .utils import random_email, random_lower_string


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    response = client.get("/api/users/me", headers=normal_user_token_headers)
    current_user = response.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_admin"] is False
    assert current_user["email"] == "test@test.ru"
    assert current_user["username"] == "test@test.ru"


def test_create_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"username": email, "email": email, "password": password}
    response = client.post(
        "/api/sign-up", headers=normal_user_token_headers, json=data,
    )
    assert 200 == response.status_code
    created_user = response.json()
    user = db.query(User).filter(User.email == email).first()
    assert user
    assert user.email == created_user["email"]
    assert user.email == email
    db.delete(user)
    db.commit()


def test_new_user_login(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"username": email, "email": email, "password": password}
    response = client.post(
        "/api/sign-up", headers=normal_user_token_headers, json=data,
    )
    assert 200 == response.status_code
    created_user = response.json()
    user = db.query(User).filter(User.email == email).first()
    assert user
    assert user.email == created_user["email"]
    assert user.email == email
    data = {"username": email, "password": password}
    response = client.post("/api/token", data=data)
    data_token = response.json()
    assert "access_token" in data_token
    db.delete(user)
    db.commit()
