from models.nutrition import nutrition_api
from flask import Flask, jsonify, request
from db_utils import (
    add_new_smoothie_db,
    add_ingredient_db,
    add_ingredient_to_smoothie_db,
    helper_get_smoothie_and_ingredient_names,
    helper_ingredient_exists,
    helper_smoothie_exists,
    delete_smoothie_by_id,
    delete_ingredients_by_id
)

app = Flask(__name__)

# GET /smoothies (all smoothies)
# GET /smoothie/smoothie_id (ex. “Banana-Strawberry Blast”)
# GET /smoothies/ingredients (all ingredients: “Banana, Strawberries, Yogurt, Milk”)
# GET /ingredients/ingredient_id/nutrition (“Banana - Per 100ml: Calories 50, Fat: 5g, Carbs: 10g Protein: 20g”)

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




@app.route("/smoothies", methods=["POST"])
def add_new_smoothie_back_end():
    """
    Create a new smoothie by a str and return a confirmation message.
    :return:A message confirming that the new smoothie was added.
    """
    data = request.get_json()
    add_new_smoothie_db(data)
    return "New smoothie created."


@app.route('/ingredients', methods=["POST"])
def add_ingredient_app():
    """
    Add an ingredient to the db from external api, if it does not already exist.
    :return: A message confirming that the ingredient was added to the db.
    """
    input_data = request.get_json()

    # user input validation
    if not input_data or 'ingredient_name' not in input_data:
        return jsonify({"error" : "Please provide a fruit name"}), 400
    if not isinstance(input_data["ingredient_name"], str):
        return jsonify({"error" : "Fruit must be of type string"}), 400

    # call external api
    try:
        fruit_data = nutrition_api.search_ingredient(input_data["ingredient_name"])
    except ValueError as error:
        return jsonify({"error" : f"Fruit, '{input_data["ingredient_name"]}', cannot be found in Fruityvice"}), 404

    except ConnectionError as error:
        return jsonify({"error": "Failed to connect to 'Fruityvice' API"}), 503

    ingredient_id = add_ingredient_db(fruit_data)

    if ingredient_id:
        return jsonify({
            "ingredient_id" :  ingredient_id,
            "message" : f"{fruit_data['ingredient_name']} added successfully"
        }), 201

    return jsonify({"error" : "Failed to add ingredient. Already in database."}), 500


@app.route('/smoothies/<int:smoothie_id>/ingredients', methods=["POST"])
def add_ingredient_to_smoothie_app(smoothie_id):
    """
    Add an ingredient and ingredient units to unique smoothie from db.
    :param smoothie_id:
    :return: A message confirming that the ingredient and ingredient's units was added to the db.
    """
    # parameter error handling.
    if not isinstance(smoothie_id, int):
        return jsonify({"error" : "Must provide smoothie_id"})

    if not helper_smoothie_exists(smoothie_id):
        return jsonify({"error" : "Smoothie ID not found"}), 404

    input_data = request.get_json()

    # user input error handling.
    if not input_data or "ingredient_id" not in input_data or "grams" not in input_data:
        return jsonify({"error" : "Missing fields"}), 400

    if not helper_ingredient_exists(input_data["ingredient_id"]):
        return jsonify({"error" : "Ingredient not found"}), 404

    if not input_data or "ingredient_id" not in input_data or "grams" not in input_data:
        return jsonify({"error" : "Missing required fields"}), 400

    if not isinstance(input_data["ingredient_id"], int) or not isinstance(input_data["grams"], (int, float)):
        return jsonify({"error" : "Ingredient ID must be of type integer. Grams must be a number."}), 400

    if input_data["grams"] <= 0:
        return jsonify({"error" : "Grams must be greater than zero."}), 400

    # get data from db_utils.
    result = add_ingredient_to_smoothie_db(smoothie_id, input_data["ingredient_id"], input_data["grams"])

    if result:
        # get the names of the smoothie and ingredient.
        smoothie_name, ingredient_name = helper_get_smoothie_and_ingredient_names(smoothie_id, input_data[
            "ingredient_id"])
        return jsonify({"message" : f"{input_data["grams"]} grams of {ingredient_name} added to {smoothie_name}!"}), 201

    return jsonify({"error" : "Failed to add ingredient to smoothie"}), 500


@app.route("/smoothies/<int:smoothie_id>", methods=["DELETE"])
def delete_smoothie_back_end(smoothie_id):
    """
    Delete a smoothie by its id and return a confirmation message.
    :param smoothie_id: The unique id of the smoothie to delete.
    :return: A message confirming that the smoothie was deleted.
    """
    delete_smoothie_by_id(smoothie_id)
    return f"Smoothie {smoothie_id} deleted."


@app.route("/ingredients/<int:ingredients_id>", methods=["DELETE"])
def delete_ingredients_back_end(ingredients_id):
    """
    Delete an ingredient by its id and return a confirmation message.
    :param ingredients_id: The unique id of the ingredient to delete.
    :return: A message confirming that the ingredient was deleted.
    """
    delete_ingredients_by_id(ingredients_id)
    return f"Ingredient {ingredients_id} deleted."

if __name__ == "__main__":
    app.run(debug=True)
