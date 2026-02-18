"""
Initialize pagination
"""

from .mongo import MongoPaginator
from .postgres import DBPaginator

__all__ = ["MongoPaginator", "DBPaginator"]
