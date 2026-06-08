# db connection file to be added here
import mysql.connector
from mysql.connector import pooling
from flask import g

_db_pool = None

def init_db_pool(app):
    global _db_pool
    _db_pool = pooling.MySQLConnectionPool(
        pool_name="smoothie_pool",
        pool_size=5,
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME']
    )

def get_db_connection():
    if 'db_conn' not in g:
        g.db_conn = _db_pool.get_connection()
    return g.db_conn

def close_db_connection(e=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()
