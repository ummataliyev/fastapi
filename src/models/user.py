"""
User table
"""
from sqlalchemy.orm import Mapped, mapped_column

from db.storage.postgres import Base
from db.storage.postgres import IntIdPkMixin


class User(Base, IntIdPkMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(index=True)

    def __repr__(self):
        return f"<User id={self.id} name={self.name}>"
