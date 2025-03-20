"""
Database switcher
"""
from libs.environs import env

DB_TYPE = env.str('DB_TYPE', default='postgres')

if DB_TYPE == "postgres":
    from db.storage.postgres import Base, DB_URL
elif DB_TYPE == "mysql":
    from db.storage.mysql import Base, DB_URL
elif DB_TYPE == "mongo":
    Base = None
else:
    raise ValueError("Invalid DB_TYPE! Choose 'postgres', 'mysql', or 'mongo'.")
