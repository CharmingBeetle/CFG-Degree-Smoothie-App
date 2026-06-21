import mysql.connector
from config import db_config

#=============================================================================================================

def add_new_smoothie_db(new_smoothie):
    db = None
    cursor = None
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        insert_into_query = f"""
        INSERT INTO smoothies (smoothie_name)
        VALUES (%s)"""

        values = (
            new_smoothie['smoothie_name'],
        )

        cursor.execute(insert_into_query, values)
        db.commit()
        print(f"{new_smoothie['smoothie_name']} has been created.")
        return cursor.lastrowid

    except mysql.connector.Error as err:
        print(f"Oops! Something went wrong: {err}")
        db.rollback()
        return None

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

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

# =============================================================================================================

# adds new ingredient to smoothie_ingredients table
def add_ingredient_to_smoothie_db(smoothie_id, ingredient_id, grams):
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = """
               INSERT INTO smoothie_ingredients (smoothie_id, ingredient_id, grams)
               VALUES (%s, %s, %s)
           """
        values = (smoothie_id, ingredient_id, grams)

        cursor.execute(query, values)
        db.commit()

        return cursor.lastrowid

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if db:
            db.rollback()
        return None

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

def get_all_smoothies():
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query= """
            SELECT s.smoothie_id, s.smoothie_name AS name,
            GROUP_CONCAT(CONCAT(i.ingredient_name, '(', si.quantity,')') SEPARATOR ', ' ) AS ingredients
            FROM smoothies AS s
            JOIN smoothie_ingredients AS si ON s.smoothie_id = si.smoothie_id
            JOIN ingredients AS i ON i.ingredient_id = si.ingredient_id
            WHERE si.quantity > 0
            GROUP BY s.smoothie_id
        """

        cursor.execute(query)

        smoothies = cursor.fetchall()

        return smoothies

    except mysql.connector.Error as err:
        print(f"Error retrieving: {err}")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()

# =============================================================================================================

# Retrieves one smoothie based on ID, its ingredients and quantities
def get_smoothie_by_id(smoothie_id):
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT s.smoothie_id, s.smoothie_name AS name, 
            GROUP_CONCAT(CONCAT(i.ingredient_name, '(', si.quantity,')') SEPARATOR ', ' ) AS ingredients
            FROM smoothies AS s
            JOIN smoothie_ingredients AS si ON s.smoothie_id = si.smoothie_id
            JOIN ingredients AS i ON i.ingredient_id = si.ingredient_id
            WHERE s.smoothie_id = %s
            GROUP BY s.smoothie_id
        """

        cursor.execute(query, (smoothie_id, ))

        smoothie = cursor.fetchone()

        return smoothie

    except mysql.connector.Error as err:
        print(f"Error retrieving this smoothie: {err}")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()

# =============================================================================================================

# Patch - edit a smoothie
def update_smoothie_db(smoothie_id, smoothie_name):
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = """
            UPDATE smoothies
            SET smoothie_name = %s
            WHERE smoothie_id = %s
        """

        values = (smoothie_name, smoothie_id)

        cursor.execute(query, values)
        db.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if db:
            db.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

# Patch - edit a ingredient
def update_ingredient_calories_db(ingredient_id, calories):
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = """
            UPDATE ingredients
            SET calories = %s
            WHERE ingredient_id = %s
        """

        values = (calories, ingredient_id)

        cursor.execute(query, values)
        db.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if db:
            db.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

def delete_smoothie_by_id(smoothie_id):
    db = None
    cursor = None
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        delete_query = f"""
        DELETE FROM smoothies
        WHERE smoothie_id = %s """

        cursor.execute(delete_query, (smoothie_id,))
        db.commit()
        print(f"***** Smoothie {smoothie_id} Deleted *****\n")

        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        print(f"Oops! Something went wrong: {err}")
        if db is not None:
            db.rollback()
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

def delete_ingredients_by_id(ingredient_id):
    db = None
    cursor = None
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        delete_query = f"""
        DELETE FROM ingredients 
        WHERE ingredient_id = %s """

        cursor.execute(delete_query, (ingredient_id,))
        db.commit()
        print(f"***** Ingredient {ingredient_id} Deleted *****\n")

        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        print(f"Oops! Something went wrong: {err}")
        if db is not None:
            db.rollback()
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

# check if smoothie exists by id
def helper_smoothie_exists_by_id(smoothie_id):
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = "SELECT 1 FROM smoothies WHERE smoothie_id = %s"

        cursor.execute(query, (smoothie_id,))
        result = cursor.fetchone()

        if result:
            return True
        return False

    except mysql.connector.Error as error:
        print(f"Error checking database: {error}")

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

# check if smoothie exists by name
def helper_smoothie_exists_by_name(smoothie_name):
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = "SELECT 1 FROM smoothies WHERE smoothie_name = %s"

        cursor.execute(query, (smoothie_name,))
        result = cursor.fetchone()

        if result:
            return True
        return False

    except mysql.connector.Error as error:
        print(f"Error checking database: {error}")

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

# check if ingredient exists by id
def helper_ingredient_exists_by_id(ingredient_id):
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = "SELECT 1 FROM ingredients WHERE ingredient_id = %s"

        cursor.execute(query, (ingredient_id,))
        result = cursor.fetchone()

        if result:
            return True
        return False

    except mysql.connector.Error as error:
        print(f"Error checking database: {error}")

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

# helper function to get names rather than ids for UX
def helper_get_smoothie_and_ingredient_names(smoothie_id, ingredient_id):
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT s.smoothie_name, i.ingredient_name
            FROM smoothies s, ingredients i
            WHERE s.smoothie_id = %s and i.ingredient_id = %s
        """
        cursor.execute(query, (smoothie_id, ingredient_id))
        result = cursor.fetchone()

        return result["smoothie_name"], result["ingredient_name"]

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# =============================================================================================================

if __name__ == "__main__":
    print("\n***** CONNECTING TO SMOOTHIE INGREDIENTS DATABASE *****")