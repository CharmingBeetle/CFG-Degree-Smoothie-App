import mysql.connector
from config import db_config

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
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        insert_into_query = f"""
        INSERT INTO smoothies (smoothie_name)
        VALUES ("{new_smoothie['name']}")"""

        cursor.execute(insert_into_query)
        db.commit()
        print("***** NEW SMOOTHIE NAME CREATED *****")

    except mysql.connector.Error as err:
        print(f"Oops! Something went wrong: {err}")
        db.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


def add_ingredient_db(ingredient_dict):
    db = None
    cursor = None
    print(f"Adding {ingredient_dict}")

    print("Connecting to Smoothie database...")

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = """
            INSERT INTO ingredients (ingredient_name, calories, protein_g, carbohydrates_g, sugar_g, fat_g)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            ingredient_dict["ingredient_name"],
            ingredient_dict["calories"],
            ingredient_dict["protein_g"],
            ingredient_dict["carbohydrates_g"],
            ingredient_dict["sugar_g"],
            ingredient_dict["fat_g"]
        )

        cursor.execute(query, values)
        db.commit()

        ingredient_id = cursor.lastrowid
        ingredient_name = ingredient_dict["ingredient_name"]

        print(f"{ingredient_name} added successfully! ID: {ingredient_id}")
        return cursor.lastrowid

    except mysql.connector.Error as err:
        print(f"Error inserting: {err}")
        if db:
            db.rollback()
        return None

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

if __name__ == "__main__":
    print("\n***** CONNECTING TO SMOOTHIE INGREDIENTS DATABASE *****")