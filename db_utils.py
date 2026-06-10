import mysql.connector
from flask import g, current_app


def get_db_connection():
    if "db_conn" not in g:
        g.db_conn = mysql.connector.connect(
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"]
        )
    return g.db_conn


def close_db_connection(e=None):
    db_conn = g.pop("db_conn", None)
    if db_conn:
        db_conn.close()
