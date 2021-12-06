import os

import psycopg2
from psycopg2 import pool
from contextlib import contextmanager


class DbPool:

    psql_pool = None

    @classmethod
    def get_instance(cls):
        if cls.psql_pool is None:
            cls.psql_pool = psycopg2.pool.SimpleConnectionPool(
                1,
                22,
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                sslmode='require'
            )
        return cls.psql_pool


@contextmanager
def get_db_connection():
    psql_pool = DbPool.get_instance()
    connection = psql_pool.getconn()
    try:
        yield connection
    except Exception as error:
        print(error)
    finally:
        psql_pool.putconn(connection)
