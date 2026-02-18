"""
Initialize AWS
"""

from .bucket import AWS_IS_ENABLED
from .bucket import aws_client

__all__ = ["AWS_IS_ENABLED", "aws_client"]
