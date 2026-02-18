"""
Redis connection
"""
import redis.asyncio as redis

from libs.environs import env

REDIS_IS_ENABLE = env.bool("REDIS_IS_ENABLE", default=False)
redis_client = None

if REDIS_IS_ENABLE:
    redis_client = redis.Redis(
        db=env.int('REDIS_DB', default=0),
        host=env.str('REDIS_HOST', default='localhost'),
        port=env.int('REDIS_PORT', default=6379),
        password=env.str('REDIS_PASSWORD', default=None)
    )
