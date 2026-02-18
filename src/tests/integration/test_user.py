"""
Integration-like tests for user routes with dependency overrides.
"""

from datetime import datetime
from datetime import timezone
from dataclasses import dataclass

from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from src.main import app
from src.services.user import UserService


@dataclass
class DummyUser:
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class FakeUserService:
    async def get_by_id(self, record_id: int):
        if record_id == 999:
            raise ValueError("User not found")
        now = datetime.now(timezone.utc)
        return DummyUser(
            id=record_id,
            name="Alice",
            email="alice@example.com",
            created_at=now,
            updated_at=now,
        )

    async def get_all(self):
        now = datetime.now(timezone.utc)
        return [
            DummyUser(
                id=1,
                name="Alice",
                email="alice@example.com",
                created_at=now,
                updated_at=now,
            )
        ]

    async def create(self, **kwargs):
        if kwargs["email"] == "duplicate@example.com":
            raise IntegrityError("insert", kwargs, Exception("duplicate"))
        now = datetime.now(timezone.utc)
        return DummyUser(
            id=2,
            name=kwargs["name"],
            email=kwargs["email"],
            created_at=now,
            updated_at=now,
        )

    async def update(self, record_id: int, **kwargs):
        now = datetime.now(timezone.utc)
        return DummyUser(
            id=record_id,
            name=kwargs.get("name", "Alice"),
            email=kwargs.get("email", "alice@example.com"),
            created_at=now,
            updated_at=now,
        )

    async def delete(self, record_id: int):
        if record_id == 999:
            raise ValueError("User not found")
        return {"message": "deleted"}


def _override_user_service():
    return FakeUserService()


def test_get_user_not_found_returns_404():
    app.dependency_overrides[UserService.get_service] = _override_user_service
    with TestClient(app) as client:
        response = client.get("/users/999")
    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["message"] == "User not found"


def test_create_user_conflict_returns_409():
    app.dependency_overrides[UserService.get_service] = _override_user_service
    with TestClient(app) as client:
        response = client.post(
            "/users/",
            json={"name": "Bob", "email": "duplicate@example.com"},
        )
    app.dependency_overrides.clear()

    assert response.status_code == 409
    assert response.json()["message"] == "User with this email already exists"


def test_create_user_success_returns_201():
    app.dependency_overrides[UserService.get_service] = _override_user_service
    with TestClient(app) as client:
        response = client.post(
            "/users/",
            json={"name": "Bob", "email": "bob@example.com"},
        )
    app.dependency_overrides.clear()

    payload = response.json()
    assert response.status_code == 201
    assert payload["status"] == "success"
    assert payload["data"]["email"] == "bob@example.com"
