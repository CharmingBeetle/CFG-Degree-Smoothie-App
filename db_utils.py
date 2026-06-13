from mysql.connector import connect
from flask import g, current_app


def get_db_connection():
    if "db_conn" not in g:
        g.db_conn = connect(
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

# Retrieves all smoothies, their ingredients and quantities
def get_all_smoothies():
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)

    sql_query= """
        SELECT s.smoothie_id, s.smoothie_name AS name,
        GROUP_CONCAT(CONCAT(i.ingredient_name, '(', si.quantity,')') SEPARATOR ', ' ) AS ingredients
        FROM smoothies AS s
        JOIN smoothie_ingredients AS si ON s.smoothie_id = si.smoothie_id
        JOIN ingredients AS i ON i.ingredient_id = si.ingredient_id
        WHERE si.quantity > 0
        GROUP BY s.smoothie_id
    """

    cursor.execute(sql_query)

    smoothies = cursor.fetchall()

    cursor.close()
    return smoothies

# Retrieves one smoothie based on ID, its ingredients and quantities
def get_smoothie_by_id(smoothie_id):
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)

    sql_query = """
        SELECT s.smoothie_id, s.smoothie_name AS name, 
        GROUP_CONCAT(CONCAT(i.ingredient_name, '(', si.quantity,')') SEPARATOR ', ' ) AS ingredients
        FROM smoothies AS s
        JOIN smoothie_ingredients AS si ON s.smoothie_id = si.smoothie_id
        JOIN ingredients AS i ON i.ingredient_id = si.ingredient_id
        WHERE s.smoothie_id = %s
        GROUP BY s.smoothie_id
    """

    cursor.execute(sql_query, (smoothie_id, ))

    smoothie = cursor.fetchone()

    return smoothie




