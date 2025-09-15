"""
Soft Deletion Mixin for SQLAlchemy Models
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class SoftDeletionMixin:
    """
    Adds soft deletion support with helper methods.
    """

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    def soft_delete(self) -> None:
        """
        Mark record as deleted.
        """
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        """
        Restore a soft-deleted record.
        """
        self.deleted_at = None

    @property
    def is_deleted(self) -> bool:
        """
        Check if record is soft deleted.
        """
        return self.deleted_at is not None
