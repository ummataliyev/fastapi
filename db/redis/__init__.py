"""
Initialize Redis
"""

from .broker import REDIS_IS_ENABLE
from .broker import redis_client

__all__ = ["REDIS_IS_ENABLE", "redis_client"]
