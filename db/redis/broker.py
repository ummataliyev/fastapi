"""
Redis connection
"""
import redis

from libs.environs import env

REDIS_IS_ENABLE = env.bool("REDIS_IS_ENABLE", default=False)

if REDIS_IS_ENABLE:
    redis_client = redis.Redis(
        db=env.str('REDIS_DB'),
        host=env.str('REDIS_HOST'),
        port=env.int('REDIS_PORT'),
        password=env.str('REDIS_PASSWORD')
    )
