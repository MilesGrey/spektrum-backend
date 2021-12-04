import psycopg2
from contextlib import contextmanager


@contextmanager
def get_db_connection():
    connection = psycopg2.connect(
        dbname='defaultdb',
        user='doadmin',
        password='p3stzq1xpfhnmdlr',
        host='db-spektrum-do-user-4221323-0.b.db.ondigitalocean.com',
        port='25060',
        sslmode='require'
    )
    try:
        yield connection
    finally:
        connection.close()
