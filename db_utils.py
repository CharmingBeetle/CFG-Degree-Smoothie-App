import mysql.connector
from config import config

# from mysql.connector import pooling
# from flask import g
#
# _db_pool = None
#
# def init_db_pool(app):
#     global _db_pool
#     _db_pool = pooling.MySQLConnectionPool(
#         pool_name="smoothie_pool",
#         pool_size=5,
#         host=app.config['DB_HOST'],
#         user=app.config['DB_USER'],
#         password=app.config['DB_PASSWORD'],
#         database=app.config['DB_NAME']
#     )
#
# def get_db_connection():
#     if 'db_conn' not in g:
#         g.db_conn = _db_pool.get_connection()
#     return g.db_conn
#
# def close_db_connection(e=None):
#     db_conn = g.pop('db_conn', None)
#     if db_conn is not None:
#         db_conn.close()

def add_new_smoothie_db(new_smoothie):
    db = None
    cursor = None
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(dictionary=True)

        insert_into_query = f"""
        INSERT INTO smoothies (smoothie_name)
        VALUES ("{new_smoothie['name']}")"""

        cursor.execute(insert_into_query)
        results = cursor.fetchall()
        db.commit()
        print("***** NEW SMOOTHIE NAME CREATED *****")
        return results

    except mysql.connector.Error as err:
        print(f"Oops! Something went wrong: {err}")
        db.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

if __name__ == "__main__":
    print("\n***** CONNECTING TO SMOOTHIE INGREDIENTS DATABASE *****")