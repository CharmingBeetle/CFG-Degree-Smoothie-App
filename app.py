from models.nutrition import nutrition_api
from flask import Flask, jsonify, request
from db_utils import (
    add_new_smoothie_db,
    add_ingredient_db,
    add_ingredient_to_smoothie_db,
    helper_get_smoothie_and_ingredient_names,
    helper_ingredient_exists_by_id,
    helper_smoothie_exists_by_id,
    delete_smoothie_by_id,
    delete_ingredients_by_id,
    update_smoothie_db,
    update_ingredient_db,
    helper_smoothie_exists_by_name,
    get_all_smoothies,
    get_smoothie_by_id_db,
    get_all_ingredients,
    get_ingredient_by_id_db
)

app = Flask(__name__)

@app.route('/smoothies', methods=['GET'])
def get_smoothies():
    """
    Get all smoothies from database.
    :return: A list of all smoothies from MySQL database.
    """
    smoothies = get_all_smoothies()

    if smoothies is None:
        return jsonify({"error": "Failed to retrieve smoothies. PLease try again."}), 500

    return jsonify(smoothies), 200

#======================================================================================================

@app.route('/smoothies/<int:smoothie_id>', methods=['GET'])
def get_smoothie_by_id(smoothie_id):
    """
    Get smoothie by id.
    :param smoothie_id:
    :return: A single smoothie from the MySQL database.
    """
    smoothie = get_smoothie_by_id_db(smoothie_id)
    if smoothie:
        return jsonify(smoothie), 200
    return jsonify({"error": f"Smoothie with id {smoothie_id} not found. Please try again."}), 404

#======================================================================================================

@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    """
    Get all ingredients from database.
    :return: A list of all ingredients from MySQL database.
    """
    ingredients = get_all_ingredients()

    if ingredients is None:
        return jsonify({"error": "Failed to retrieve ingredients. Please try again."}), 500

    return jsonify(ingredients), 200

#======================================================================================================

@app.route('/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient_by_id(ingredient_id):
    """
    Get ingredient by id.
    :param ingredient_id:
    :return: A single ingredient from the MySQL database.
    """
    ingredient = get_ingredient_by_id_db(ingredient_id)
    if ingredient:
        return jsonify(ingredient), 200
    return jsonify({"error": f"Ingredient with id {ingredient_id} not found. Please try again."}), 404

#=============================================================================================================

@app.route("/smoothies", methods=["POST"])
def add_new_smoothie_back_end():
    """
    Create a new smoothie by a str and return a confirmation message.
    :return:A message confirming that the new smoothie was added.
    """
    input_data = request.get_json()

    if not input_data or 'smoothie_name' not in input_data:
        return jsonify({"error": "Smoothie name is required."}), 400

    if not isinstance(input_data["smoothie_name"], str):
        return jsonify({"error": "Smoothie name must be a string. Please try again."}), 400

    if not input_data["smoothie_name"].strip():
        return jsonify({"error" : "Smoothie name must not be empty. Please try again."}), 400

    if helper_smoothie_exists_by_name(input_data["smoothie_name"]):
        return jsonify({"error": "A smoothie with that name already exists. Please try again."}), 409

    smoothie_id = add_new_smoothie_db(
        input_data
    )

    if smoothie_id:
        return jsonify({
            "smoothie_id" :  smoothie_id,
            "message" : f"{input_data['smoothie_name']} added successfully."
        }), 201

    return jsonify({"error" : "There was an internal error. Failed to add smoothie. Please try again."}), 500

#=============================================================================================================

@app.route('/ingredients', methods=["POST"])
def add_ingredient_app():
    """
    Add an ingredient to the db from external api, if it does not already exist.
    :return: A message confirming that the ingredient was added to the db.
    """
    input_data = request.get_json()

    if not input_data or 'ingredient_name' not in input_data:
        return jsonify({"error" : "Ingredient name is required."}), 400

    if not isinstance(input_data["ingredient_name"], str):
        return jsonify({"error": "Ingredient name must be a string. Please try again."}), 400

    if not input_data["ingredient_name"].strip():
        return jsonify({"error": "Ingredient name must not be empty. Please try again."}), 400

    try:
        fruit_data = nutrition_api.search_ingredient(input_data["ingredient_name"])
    except ValueError as error:
        return jsonify({"error" : f"Ingredient, '{input_data['ingredient_name']}', cannot be found in external database - Fruityvice. Please try again."}), 404

    except ConnectionError as error:
        return jsonify({"error": "Failed to connect to external database - Fruityvice. Please try again."}), 503

    ingredient_id = add_ingredient_db(
        fruit_data
    )

    if ingredient_id:
        return jsonify({
            "ingredient_id" :  ingredient_id,
            "message" : f"{fruit_data['ingredient_name']} added successfully."
        }), 201

    return jsonify({"error" : "There was an external error. Failed to add ingredient. Please try again."}), 500

#=============================================================================================================

@app.route('/smoothies/<int:smoothie_id>/ingredients', methods=["POST"])
def add_ingredient_to_smoothie_app(smoothie_id):
    """
    Add an ingredient and ingredient units to unique smoothie from db.
    :param smoothie_id:
    :return: A message confirming that the ingredient and ingredient's units was added to the db.
    """

    if not helper_smoothie_exists_by_id(smoothie_id):
        return jsonify({"error" : "Smoothie ID not found"}), 404

    input_data = request.get_json()

    if not input_data or "ingredient_id" not in input_data or "grams" not in input_data:
        return jsonify({"error" : "Missing required fields."}), 400

    if not isinstance(input_data["ingredient_id"], int) or not isinstance(input_data["grams"], (int, float)):
        return jsonify({"error": "Ingredient ID must be a number. Grams must be numeric."}), 400

    if input_data["grams"] <= 0:
        return jsonify({"error" : "Grams must be greater than zero."}), 400

    if not helper_ingredient_exists_by_id(input_data["ingredient_id"]):
        return jsonify({"error" : "Ingredient not found."}), 404

    smoothie_ingredient_id = add_ingredient_to_smoothie_db(
        smoothie_id,
        input_data["ingredient_id"],
        input_data["grams"]
    )

    if smoothie_ingredient_id:
        smoothie_name, ingredient_name = helper_get_smoothie_and_ingredient_names(smoothie_id, input_data[
            "ingredient_id"]
        )

        return jsonify({
            "message" : f"{input_data["grams"]} grams of {ingredient_name} added to {smoothie_name}!"
        }), 201

    return jsonify({"error" : "Failed to add ingredient to smoothie"}), 500

#=============================================================================================================

# PATCH /smoothies/smoothie_id (edit a smoothie)
@app.route("/smoothies/<int:smoothie_id>", methods=["PATCH"])
def update_smoothie(smoothie_id):

    data = request.get_json()

    if not data or "smoothie_name" not in data:
        return jsonify({"error": "Missing required field"}), 400

    smoothie_name = data.get("smoothie_name")

    if not isinstance(smoothie_name, str):
        return jsonify({"error": "Smoothie name must be text"}), 400

    if smoothie_name.strip() == "":
        return jsonify({"error": "Smoothie name cannot be empty"}), 400

    update_smoothie_db(smoothie_id, smoothie_name)

    return jsonify({
        "message": "Smoothie updated",
        "smoothie_id": smoothie_id,
        "new_name": smoothie_name
    }), 200



# PATCH /ingredients/ingredient_id (edit ingredient)
@app.route("/ingredients/<int:ingredient_id>", methods=["PATCH"])
def update_ingredient(ingredient_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing required fields"}), 400

    allowed_fields = [
        "ingredient_name",
        "calories",
        "protein_g",
        "carbohydrates_g",
        "sugar_g",
        "fat_g"
    ]

    update_data = {}

    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]

    if not update_data:
        return jsonify({"error": "No valid fields provided"}), 400

    if "ingredient_name" in update_data:
        if not isinstance(update_data["ingredient_name"], str):
            return jsonify({"error": "Ingredient name must be text"}), 400

        if update_data["ingredient_name"].strip() == "":
            return jsonify({"error": "Ingredient name cannot be empty"}), 400

    nutrition_fields = [
        "calories",
        "protein_g",
        "carbohydrates_g",
        "sugar_g",
        "fat_g"
    ]

    for field in nutrition_fields:
        if field in update_data:
            if not isinstance(update_data[field], (int, float)):
                return jsonify({"error": f"{field} must be a number"}), 400

            if update_data[field] < 0:
                return jsonify({"error": f"{field} cannot be negative"}), 400

    update_ingredient_db(ingredient_id, update_data)

    return jsonify({
        "message": "Ingredient updated",
        "ingredient_id": ingredient_id,
        "updated_data": update_data
    }), 200

#=============================================================================================================

@app.route("/smoothies/<int:smoothie_id>", methods=["DELETE"])
def delete_smoothie_back_end(smoothie_id):
    """
    Delete a smoothie by its id and return a confirmation message.
    :param smoothie_id: The unique id of the smoothie to delete.
    :return: A message confirming that the smoothie was deleted.
    """

    if not helper_smoothie_exists_by_id(smoothie_id):
        return jsonify({"error": "A smoothie with that id does not exist."}), 404

    is_deleted = delete_smoothie_by_id(
        smoothie_id
    )

    if is_deleted:
        return jsonify({
            "message": f"Smoothie {smoothie_id} deleted",
        }), 200

    return jsonify({"error" : "Failed to delete smoothie id. There was an internal error. Please try again."}), 500

#=============================================================================================================

@app.route("/ingredients/<int:ingredient_id>", methods=["DELETE"])
def delete_ingredients_back_end(ingredient_id):
    """
    Delete an ingredient by its id and return a confirmation message.
    :param ingredient_id: The unique id of the ingredient to delete.
    :return: A message confirming that the ingredient was deleted.
    """
    if not helper_ingredient_exists_by_id(ingredient_id):
        return jsonify({"error": "An ingredient with that id does not exist."}), 404

    is_deleted = delete_ingredients_by_id(
        ingredient_id
    )

    if is_deleted:
        return jsonify({
            "message": f"Ingredient {ingredient_id} deleted",
        }), 200

    return jsonify({"error" : "Failed to delete ingredient id. There was an internal error. Please try again."}), 500

#=============================================================================================================

if __name__ == "__main__":
    app.run(debug=True)