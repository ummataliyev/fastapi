"""
Redis connection
"""
import redis

from libs.environs import env


REDIS_DB = env.str('REDIS_DB')
REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.int('REDIS_PORT')
REDIS_PASSWORD = env.str('REDIS_PASSWORD')

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB
)
