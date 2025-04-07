"""
User table
"""
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from db.storage.postgres import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    name = Column(String, index=True)

    def __repr__(self):
        return f"<Item id={self.id} name={self.name}>"
