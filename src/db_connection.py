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
                dbname='defaultdb',
                user='doadmin',
                password='p3stzq1xpfhnmdlr',
                host='db-spektrum-do-user-4221323-0.b.db.ondigitalocean.com',
                port='25060',
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
