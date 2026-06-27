import requests

#=============================================================================================================

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def add_ingredient_to_smoothie(self, smoothie_id, ingredient_id, grams):
        data_to_send = {
            "ingredient_id": ingredient_id,
            "grams": grams
        }

        return requests.post(
            f"{self.base_url}/smoothies/{smoothie_id}/ingredients",
            json=data_to_send
        )

# =============================================================================================================

    def create_new_smoothie(self, smoothie_name):
        smoothie = {"smoothie_name": smoothie_name}
        return requests.post(f"{self.base_url}/smoothies", json=smoothie)

# =============================================================================================================

    def get_smoothie_by_id(self, smoothie_id):
        return requests.get(f"{self.base_url}/smoothies/{smoothie_id}")

# =============================================================================================================

    def get_all_smoothies(self):
        return requests.get(f"{self.base_url}/smoothies")

# =============================================================================================================

    def get_all_ingredients(self):
        return requests.get(f"{self.base_url}/ingredients")

# =============================================================================================================

    def update_smoothie_name(self, smoothie_id, smoothie_name):
        data_to_send = {
            "smoothie_name": smoothie_name
        }
        return requests.patch(f"{self.base_url}/smoothies/{smoothie_id}", json=data_to_send)

# =============================================================================================================

    def delete_smoothie(self, smoothie_id):
        return requests.delete(f"{self.base_url}/smoothies/{smoothie_id}")

# =============================================================================================================

    def get_ingredients_by_id(self, ingredient_id):
        return requests.get(f"{self.base_url}/ingredients/{ingredient_id}")

# =============================================================================================================

    def create_new_ingredient(self, ingredient_name):
        ingredient = {"ingredient_name": ingredient_name}
        return requests.post(f"{self.base_url}/ingredients", json=ingredient)

# =============================================================================================================

    def update_ingredient(self, ingredient_id, ingredient_name, calories, protein, carbohydrates, sugar, fat):
        data_to_send: dict[str, object] = {
            "ingredient_name": ingredient_name,
            "calories": calories,
            "protein_g": protein,
            "carbohydrates_g": carbohydrates,
            "sugar_g": sugar,
            "fat_g": fat
        }
        return requests.patch(f"{self.base_url}/ingredients/{ingredient_id}", json=data_to_send)

# =============================================================================================================

    def delete_ingredient(self, ingredient_id):
        return requests.delete(f"{self.base_url}/ingredients/{ingredient_id}")