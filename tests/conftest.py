from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db import SessionLocal
from main import app
from .utils import (
    user_authentication_headers,
    create_test_user,
    delete_test_user,
    get_test_user_id
)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client(db: Session) -> Generator:
    with TestClient(app) as c:
        create_test_user(db)
        yield c
        delete_test_user(db)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return user_authentication_headers(
        client=client, username="test@test.ru", password="test"
    )


@pytest.fixture(scope="module")
def user_id(client: TestClient, db: Session) -> int:
    return get_test_user_id(db)
