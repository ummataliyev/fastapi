"""
User Table
"""

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.storage.postgres import Base
from db.storage.postgres.mixins import IntIdPkMixin
from db.storage.postgres.mixins import TimestampMixin
from db.storage.postgres.mixins import SoftDeletionMixin


class User(Base, IntIdPkMixin, TimestampMixin, SoftDeletionMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(index=True)

    def __repr__(self):
        return f"<User id={self.id} name={self.name}>"
