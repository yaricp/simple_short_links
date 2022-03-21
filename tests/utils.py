import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional

from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from settings import SHORT_LINK_EXPIRE_DAYS
from models.link import Link as LinkModel
from models.user import User as UserModel
from utils.links import get_short_url
from utils.users import get_password_hash


def random_lower_string() -> str:
    """Generates random string for tests"""
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    """Generates random email for tests"""
    return f"{random_lower_string()}@{random_lower_string()}.com"


def user_authentication_headers(
    *, client: TestClient, username: str, password: str
) -> Dict[str, str]:
    """Gets header with token after user authentification"""
    data = {"username": username, "password": password}
    r = client.post("/api/token", data=data)
    response = r.json()
    if "access_token" not in response:
        return {}
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_test_user_id(db: Session) -> Optional[int]:
    """Gets test user id for database"""
    return db.query(UserModel).filter(
        UserModel.email == "test@test.ru"
    ).first().id


def create_random_user(db: Session) -> UserModel:
    """Creates random user for tests"""
    email = random_email()
    password = random_lower_string()
    user_in = UserModel(username=email, email=email, password=password)
    db.add(user_in)
    db.commit()
    return user_in


def create_test_user(db: Session) -> None:
    """Creates test user for test links"""
    email = "test@test.ru"
    user_in = UserModel(
        username=email,
        email=email,
        password=get_password_hash("test")
    )
    db.add(user_in)
    db.commit()


def delete_test_user(db: Session) -> None:
    """Deletes test user after test"""
    db_obj = db.query(UserModel).filter(UserModel.email == "test@test.ru").first()
    db.delete(db_obj)
    db.commit()


def create_random_link(db: Session, *, owner_id: Optional[int] = None) -> LinkModel:
    """Creates random link for tests"""
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    text = "http://%s" % random_lower_string()
    item_in = LinkModel(
        text=text,
        short_text=get_short_url(text),
        expired=datetime.utcnow() + timedelta(days=SHORT_LINK_EXPIRE_DAYS),
        owner_id=owner_id
    )
    db.add(item_in)
    db.commit()
    db.refresh(item_in)
    return item_in
