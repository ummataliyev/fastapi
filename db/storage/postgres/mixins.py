"""
Database models mixins
"""
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class IntIdPkMixin:
    """
    Mixin is a primary key of type int.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
