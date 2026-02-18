"""
Unit tests for UserService
"""

import pytest

from unittest.mock import patch
from unittest.mock import AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.services.user import UserService


@pytest.fixture
def service() -> UserService:
    """
    Build UserService with a mocked DB session.
    """
    mock_db = AsyncMock(spec=AsyncSession)
    return UserService(db=mock_db)


@pytest.mark.anyio
async def test_create_user(service: UserService):
    """
    Test that UserService.create correctly calls repository.create
    and returns a User object.
    """
    user_data = {"id": 1, "name": "testuser", "email": "test@example.com"}
    mock_user = User(**user_data)

    with patch.object(
        service.repository, "create", AsyncMock(return_value=mock_user)
    ) as mock_create:
        result = await service.create(**user_data)
        mock_create.assert_awaited_once_with(obj_in=user_data)
        assert result.id == 1
        assert result.name == "testuser"
        assert result.email == "test@example.com"


@pytest.mark.anyio
async def test_get_user_by_id(service: UserService):
    """
    Test that UserService.get_by_id correctly calls repository.get
    and returns the expected User object.
    """
    mock_user = User(id=1, name="testuser", email="test@example.com")

    with patch.object(
        service.repository, "get", AsyncMock(return_value=mock_user)
    ) as mock_get:
        result = await service.get_by_id(1)
        mock_get.assert_awaited_once_with(id=1)
        assert result.name == "testuser"


@pytest.mark.anyio
async def test_update_user(service: UserService):
    """
    Test that UserService.update correctly calls repository.update
    with the correct parameters and returns the updated User object.
    """
    existing_user = User(id=1, name="testuser", email="test@example.com")
    updated_data = {"name": "updateduser"}

    with patch.object(
        service.repository, "get", AsyncMock(return_value=existing_user)
    ), patch.object(
        service.repository,
        "update",
        AsyncMock(
            return_value=User(
                id=1,
                name="updateduser",
                email="test@example.com",
            )
        ),
    ) as mock_update:
        result = await service.update(1, **updated_data)
        mock_update.assert_awaited_once_with(
            obj_current=existing_user,
            obj_in=updated_data,
        )
        assert result.name == "updateduser"


@pytest.mark.anyio
async def test_delete_user(service: UserService):
    """
    Test that UserService.delete correctly calls repository.delete
    and returns the expected success message.
    """
    with patch.object(
        service.repository,
        "delete",
        AsyncMock(return_value=None),
    ) as mock_delete:
        result = await service.delete(1)
        mock_delete.assert_awaited_once_with(id=1)
        assert result == {"message": "User with id 1 deleted successfully"}
