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
    update_ingredient_calories_db,
    helper_smoothie_exists_by_name
)

app = Flask(__name__)

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
        return jsonify({"error": "Smoothie name must contain only letters. Please try again."}), 400

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
    if not input_data["ingredient_name"].isalpha():
        return jsonify({"error" : "Ingredient name must contain only letters and it must be a string. Please try again."}), 400

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

    result = add_ingredient_to_smoothie_db(
        smoothie_id,
        input_data["ingredient_id"],
        input_data["grams"]
    )

    if result:
        smoothie_name, ingredient_name = helper_get_smoothie_and_ingredient_names(smoothie_id, input_data[
            "ingredient_id"]
        )

        return jsonify({
            "message" : f"{input_data["grams"]} grams of {ingredient_name} added to {smoothie_name}!"
        }), 201

    return jsonify({"error" : "Failed to add ingredient to smoothie"}), 500

#=============================================================================================================

# GET /smoothies (all smoothies)
# GET /smoothie/smoothie_id (ex. “Banana-Strawberry Blast”)
# GET /smoothies/ingredients (all ingredients: “Banana, Strawberries, Yogurt, Milk”)
# GET /ingredients/ingredient_id/nutrition (“Banana - Per 100ml: Calories 50, Fat: 5g, Carbs: 10g Protein: 20g”)

#=============================================================================================================

# PATCH /smoothies/smoothie_id (edit a smoothie)
@app.route("/smoothies/<int:smoothie_id>", methods=["PATCH"])
def update_smoothie(smoothie_id):
    data = request.get_json()

    smoothie_name = data.get("smoothie_name")

    update_smoothie_db(smoothie_id, smoothie_name)

    return jsonify({
        "message": "Smoothie updated",
        "smoothie_id": smoothie_id,
        "new_name": smoothie_name
    })

#=============================================================================================================

# PATCH /ingredients/ingredient_id (edit ingredient)
@app.route("/ingredients/<int:ingredient_id>", methods=["PATCH"])
def update_ingredient(ingredient_id):
    data = request.get_json()

    calories = data.get("calories")

    update_ingredient_calories_db(ingredient_id, calories)

    return jsonify({
        "message": "Ingredient updated",
        "ingredient_id": ingredient_id,
        "updated_calories": calories
    })

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

    result = delete_smoothie_by_id(
        smoothie_id
    )

    if result:
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

    result = delete_ingredients_by_id(
        ingredient_id
    )

    if result:
        return jsonify({
            "message": f"Ingredient {ingredient_id} deleted",
        }), 204

    return jsonify({"error" : "Failed to delete ingredient id. There was an internal error. Please try again."}), 500

#=============================================================================================================

if __name__ == "__main__":
    app.run(debug=True)
