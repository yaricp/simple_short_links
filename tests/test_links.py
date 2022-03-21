from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.link import Link

from .utils import create_random_link


def test_create_link(
    client: TestClient,
    normal_user_token_headers: dict,
    user_id: int,
    db: Session
) -> None:
    """test for create link"""
    data = {"text": "http://Foo"}
    response = client.post(
        "/api/links", headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == data["text"]
    assert content["owner_id"] == user_id
    assert content["text"].find("http://") != -1
    assert content["short_text"].find("http://") == -1
    assert "id" in content
    assert "owner_id" in content
    db_obj = db.query(Link).get(content["id"])
    db.delete(db_obj)
    db.commit()


def test_read_link(
    client: TestClient,
    normal_user_token_headers: dict,
    db: Session,
    user_id: int
) -> None:
    """test for read link"""
    item = create_random_link(db, owner_id=user_id)
    response = client.get(
        f"/api/link/{item.id}", headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == item.text
    assert content["short_text"] == item.short_text
    assert content["id"] == item.id
    assert content["owner_id"] == user_id


def test_update_link(
    client: TestClient,
    normal_user_token_headers: dict,
    db: Session,
    user_id: int
) -> None:
    """test for update link"""
    item = create_random_link(db, owner_id=user_id)
    response = client.get(
        f"/api/link/{item.id}", headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == item.text
    assert content["short_text"] == item.short_text
    assert content["id"] == item.id
    assert content["owner_id"] == user_id
    data = {
        "short_text": "new_sort_text",
        "expired": (
                datetime.utcnow() + timedelta(days=2)
        ).strftime("%Y-%m-%dT%H:%M")
    }
    response = client.put(
        f"/api/link/{item.id}",
        headers=normal_user_token_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == item.text
    assert content["short_text"] == "new_sort_text"
    assert content["id"] == item.id
    assert item.expired != content["expired"]
    assert content["owner_id"] == user_id


def test_get_links(
    client: TestClient,
    normal_user_token_headers: dict,
    db: Session,
    user_id: int
) -> None:
    """test for get links of current user"""
    item1 = create_random_link(db, owner_id=user_id)
    item2 = create_random_link(db, owner_id=user_id)
    response = client.get(
        "/api/links", headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) > 1
    for link in content:
        assert link["owner_id"] == user_id
    assert item1.text in [link["text"] for link in content]
    assert item2.text in [link["text"] for link in content]


def test_link_redirect(
    client: TestClient,
    normal_user_token_headers: dict
) -> None:
    """test redirect from short to long link"""
    data = {"text": "http://ya.ru"}
    response = client.post(
        "/api/links", headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    response = client.get("/%s" % content["short_text"], allow_redirects=False)
    assert response.headers["location"] == "http://ya.ru"
    assert response.status_code == 307


def test_delete_link(
    client: TestClient,
    normal_user_token_headers: dict,
    user_id: int,
    db: Session
) -> None:
    """test for delete link"""
    data = {"text": "http://Foo"}
    response = client.post(
        "/api/links", headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == data["text"]
    assert content["owner_id"] == user_id
    assert content["text"].find("http://") != -1
    assert content["short_text"].find("http://") == -1
    assert "id" in content
    assert "owner_id" in content
    id = content['id']
    response = client.delete(
        f"/api/link/{id}", headers=normal_user_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["deleted"]
    db_obj = db.query(Link).get(id)
    assert not db_obj
