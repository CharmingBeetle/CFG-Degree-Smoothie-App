# flask API to be added
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
from models.nutrition import nutrition_api

app = Flask(__name__)

# GET /smoothies (all smoothies)
# GET /smoothie/smoothie_id (ex. “Banana-Strawberry Blast”)
# GET /smoothies/ingredients (all ingredients: “Banana, Strawberries, Yogurt, Milk”)
# GET /ingredients/ingredient_id/nutrition (“Banana - Per 100ml: Calories 50, Fat: 5g, Carbs: 10g Protein: 20g”)

# POST /smoothies (create new smoothie)
@app.route("/smoothies", methods=["POST"])
def add_new_smoothie_back_end():
    data = request.get_json()
    add_new_smoothie_db(data)
    return "New smoothie created."

# POST /smoothies/smoothie_id/ingredients (add an ingredient to a smoothie)
# POST /ingredients (from EXT API - adds new ingredient)

# PATCH /smoothies/smoothie_id (edit a smoothie)
# PATCH /ingredients/ingredient_id (edit ingredient)

# DELETE /smoothies/smoothie_id (delete a smoothie recipe)
@app.route("/smoothies/<int:smoothie_id>", methods=["DELETE"])
def delete_smoothie_back_end(smoothie_id):
    delete_smoothie_by_id(smoothie_id)
    return f"Smoothie {smoothie_id} deleted."

# DELETE /ingredients/ingredient_id (delete an ingredient)
@app.route("/ingredients/<int:ingredients_id>", methods=["DELETE"])
def delete_ingredients_back_end(ingredients_id):
    delete_ingredients_by_id(ingredients_id)
    return f"Ingredient {ingredients_id} deleted."


























"""
NINA: APP FUNCTIONS
INCLUDES: 
POST ROUTES: ADD_INGREDIENT_APP , ADD_INGREDIENT_TO_SMOOTHIE_APP
LINES: 59 -134
"""
#==========START=====================================================================
# add an ingredient to the DB from Fruityvice api
@app.route('/ingredients', methods=["POST"])
def add_ingredient_app():
    input_data = request.get_json()

    # user input validation
    if not input_data or 'ingredient_name' not in input_data:
        return jsonify({"error" : "Please provide a fruit name"}), 400
    if not isinstance(input_data["ingredient_name"], str):
        return jsonify({"error" : "Fruit must be of type string"}), 400

    # call Nutritionist instance ('Fruityvice' API)
    try:
        fruit_data = nutrition_api.search_ingredient(input_data["ingredient_name"])
    except ValueError as error:
        return jsonify({"error" : f"Fruit, '{input_data["ingredient_name"]}', cannot be found in Fruityvale"}), 404

    except ConnectionError as error:
        return jsonify({"error": "Failed to connect to 'Fruityvice' API"}), 503

    ingredient_id = add_ingredient_db(fruit_data)

    if ingredient_id:
        return jsonify({
            "ingredient_id" :  ingredient_id,
            "message" : f"{fruit_data['ingredient_name']} added successfully"
        }), 201

    return jsonify({"error" : "Failed to add ingredient. Already in database."}), 500

# add ingredient to specific smoothie from DB
@app.route('/smoothies/<int:smoothie_id>/ingredients', methods=["POST"])
def add_ingredient_to_smoothie_app(smoothie_id):
    # parameter error handling
    if not isinstance(smoothie_id, int):
        return jsonify({"error" : "Must provide smoothie_id"})

    if not helper_smoothie_exists(smoothie_id):
        return jsonify({"error" : "Smoothie ID not found"}), 404

    input_data = request.get_json()

    # user input error handling
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

    #get data from db_utils
    result = add_ingredient_to_smoothie_db(smoothie_id, input_data["ingredient_id"], input_data["grams"])

    if result:
        # get the names of the smoothie and ingredient
        smoothie_name, ingredient_name = helper_get_smoothie_and_ingredient_names(smoothie_id, input_data[
            "ingredient_id"])
        return jsonify({"message" : f"{input_data["grams"]} grams of {ingredient_name} added to {smoothie_name}!"}), 201

    return jsonify({"error" : "Failed to add ingredient to smoothie"}), 500
#===========END==========================================================================


if __name__ == "__main__":
    app.run(debug=True)