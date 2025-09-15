"""
User scheme
"""

from typing import Optional

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class UserBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """
    Schema for creating a user.
    """
    pass


class UserUpdate(BaseModel):
    """
    Schema for updating a user (all fields optional).
    """
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
