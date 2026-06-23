import mysql.connector
from config import db_config

#=============================================================================================================

def create_new_smoothie_db(new_smoothie):
    """
    Insert a new smoothie into the database.
    :param new_smoothie: Dictionary containing the smoothie data.
    :return:The id of the newly created smoothie or None if the insert operation fails.
    """
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

def create_new_ingredient_db(ingredient_dict):
    """
    Insert a new ingredient into the database.
    :param ingredient_dict:
    :return: The id of the newly created ingredient if the insert is successful or None if the operation fails.
    """
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

def add_new_ingredient_to_smoothie_db(smoothie_id, ingredient_id, grams):
    """
    Add an ingredient and its quantity to a smoothie in the database.
    :param smoothie_id:
    :param ingredient_id:
    :param grams:
    :return: The id of the newly created smoothie ingredient and record if the insert is successful
    or None if the operation fails.
    """
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

def get_all_smoothies_db():
    """
    Retrieve all smoothies and their ingredients from the database.
    :return: A list of dictionaries containing all smoothies and their ingredients or None if the query fails.
    """
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query= """
            SELECT s.smoothie_id, s.smoothie_name AS name,
            GROUP_CONCAT(CONCAT(i.ingredient_name, '(', si.grams,')') SEPARATOR ', ' ) AS ingredients
            FROM smoothies AS s
            JOIN smoothie_ingredients AS si ON s.smoothie_id = si.smoothie_id
            JOIN ingredients AS i ON i.ingredient_id = si.ingredient_id
            WHERE si.grams > 0
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


# Retrieves one smoothie based on ID, its ingredients and quantities
def get_smoothie_by_id_db(smoothie_id):
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT s.smoothie_id, s.smoothie_name AS name, 
            GROUP_CONCAT(CONCAT(i.ingredient_name, '(', si.grams,')') SEPARATOR ', ' ) AS ingredients
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

#=============================================================================================================

def get_all_ingredients_db():
    """
    Retrieve all ingredients from the database.
    :return: A list of dictionaries representing all ingredients or None if the query fails.
    """
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query= """
          SELECT * FROM ingredients
        """

        cursor.execute(query)

        ingredients = cursor.fetchall()

        return ingredients

    except mysql.connector.Error as err:
        print(f"Error retrieving: {err}")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()

#======================================================================================================

def get_ingredient_by_id_db(ingredient_id):
    """
    Retrieve a single ingredient from the database by its id.
    :param ingredient_id:
    :return: A dictionary representing the ingredient if found, None if no ingredient exists or if a
    database error occurs.
    """
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        query = """
           SELECT * FROM ingredients
           WHERE ingredient_id = %s 
        """

        cursor.execute(query, (ingredient_id, ))

        ingredient = cursor.fetchone()

        return ingredient

    except mysql.connector.Error as err:
        print(f"Error retrieving this ingredient: {err}")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()

#=============================================================================================================

def update_smoothie_db(smoothie_id, smoothie_name):
    """
    Update the name of a smoothie in the database.
    :param smoothie_id:
    :param smoothie_name:
    :return: None. The function updates the database directly.
    """
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

#=============================================================================================================

def update_ingredient_db(ingredient_id, update_data):
    """
    Partially update an ingredient in the database.
    :param: ingredient_id:
    :return: Indicates whether the update operation was successful or whether the database record was updated.
    """
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        set_values = []
        values = []

        for field, value in update_data.items():
            set_values.append(f"{field} = %s")
            values.append(value)

        values.append(ingredient_id)

        query = f"""
            UPDATE ingredients
            SET {", ".join(set_values)}
            WHERE ingredient_id = %s
        """

        cursor.execute(query, values)
        db.commit()
        print(f"***** Database Updated *****\n")
        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if db:
            db.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

#=============================================================================================================

def delete_smoothie_by_id_db(smoothie_id):
    """
    Delete a smoothie from the database by its id.
    :param smoothie_id:
    :return: Indicates whether the smoothie was successfully deleted or if the operation failed.
    """
    db = None
    cursor = None
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        delete_query = """
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

def delete_ingredients_by_id_db(ingredient_id):
    """
    Delete an ingredient from the databae using its id.
    :param ingredient_id:
    :return: Indicates whether the outcome of the delete operation wa successful, no matching record or failure.
    """
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

def helper_smoothie_exists_by_id_db(smoothie_id):
    """
    Check whether a smoothie exists in the database by its id.
    :param smoothie_id:
    :return: Whether the smoothie exists in the database.
    """
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

def helper_smoothie_exists_by_name_db(smoothie_name):
    """
    Check whether a smoothie exists in the database by its name.
    :param smoothie_name:
    :return: Whether a smoothie with that name exists in the database.
    """
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

def helper_ingredient_exists_by_id_db(ingredient_id):
    """
    Check whether an ingredient exists in the database by its ID.
    :param ingredient_id:
    :return: Whether the ingredient exists in the database.
    """
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

def helper_get_smoothie_and_ingredient_name_db(smoothie_id, ingredient_id):
    """
    Retrieve the names of a smoothie and an ingredient from the database.
    :param smoothie_id:
    :param ingredient_id:
    :return: A tuple containing the smoothie name and ingredient name.
    """
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
