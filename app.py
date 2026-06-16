# flask API to be added
from flask import Flask, jsonify, request
from db_utils import (
    add_new_smoothie_db,
    add_ingredient_db
)
from models.nutrition import nutrition_api

app = Flask(__name__)

# GET /smoothies (all smoothies)
# GET /smoothie/smoothie_id (ex. “Banana-Strawberry Blast”)
# GET /smoothies/ingredients (all ingredients: “Banana, Strawberries, Yogurt, Milk”)
# GET /ingredients/ingredient_id/nutrition (“Banana - Per 100ml: Calories 50, Fat: 5g, Carbs: 10g Protein: 20g”)

# POST /smoothies (create new smoothie)
# POST /smoothies/smoothie_id/ingredients (add an ingredient to a smoothie)
# POST /ingredients (from EXT API - adds new ingredient)

# PATCH /smoothies/smoothie_id (edit a smoothie)
# PATCH /ingredients/ingredient_id (edit ingredient)

# DELETE /smoothies/smoothie_id (delete a smoothie recipe)
# DELETE /ingredients/ingredient_id (delete an ingredient)

@app.route("/smoothie", methods=["POST"])
def add_new_smoothie_back_end():
    data = request.get_json()
    add_new_smoothie_db(data)
    return "New smoothie created."



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
        return jsonify({"error" : f"Fruit, '{input_data["ingredient_name"]}', cannot be found"}), 404

    except ConnectionError as error:
        return jsonify({"error": "Failed to connect to 'Fruityvice' API"}), 503

    ingredient_id = add_ingredient_db(fruit_data)

    if ingredient_id:
        return jsonify({
            "ingredient_id" :  ingredient_id,
            "message" : f"{fruit_data['ingredient_name']} added successfully"
        }), 201

    return jsonify({"error" : "Failed to add ingredient. Already in database."}), 500



if __name__ == "__main__":
    app.run(debug=True)