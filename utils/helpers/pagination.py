"""
Helper function for pagination
"""
from sqlalchemy import func

from cryptography import fernet

from libs.environs import env

FERNET_KEY = env.str("FERNET_KEY")

f = fernet.Fernet(FERNET_KEY)


async def get_count(db, q, model):
    count_query = q.with_only_columns(func.count(model.id))
    count = await db.execute(count_query)
    return count.scalar_one()


async def encode_id(identifier: int) -> str:
    encoded_identifier = f.encrypt(str(identifier).encode())
    return encoded_identifier.decode()


async def decode_id(token: str) -> int:
    encoded_identifier = f.decrypt(token.encode())
    return int(encoded_identifier.decode())
