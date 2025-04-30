"""
User table
"""
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.storage.postgres import Base
from db.storage.postgres import IntIdPkMixin


class User(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(index=True)

    def __repr__(self):
        return f"<Item id={self.id} name={self.name}>"
