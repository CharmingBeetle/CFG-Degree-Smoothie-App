# flask API to be added
from flask import Flask, jsonify, request
from db_utils import add_new_smoothie_db
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
    new_smoothie = add_new_smoothie_db(data)
    return jsonify(new_smoothie)

if __name__ == "__main__":
    app.run(debug=True)