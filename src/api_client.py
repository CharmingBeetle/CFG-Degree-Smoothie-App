import requests

#=============================================================================================================

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def add_ingredient_to_smoothie(self, smoothie_id, ingredient_id, grams):
        """
        Adds a specific ingredient and the quantity to an existing smoothie.
        :param smoothie_id:
        :param ingredient_id:
        :param grams:
        :return: The server's response to the POST request.
        """
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
        """
        Creates a new smoothie api call to the back end.
        :param smoothie_name:
        :return: The server's response to the POST request.
        """
        smoothie = {"smoothie_name": smoothie_name}
        return requests.post(f"{self.base_url}/smoothies", json=smoothie)

# =============================================================================================================

    def get_smoothie_by_id(self, smoothie_id):
        """
        Retrieves details for a smoothie by its id.
        :param smoothie_id:
        :return: The server's response to the GET request.
        """
        return requests.get(f"{self.base_url}/smoothies/{smoothie_id}")

# =============================================================================================================

    def get_all_smoothies(self):
        """
        Retrieves a list of all smoothies.
        :return: The server's response to the GET request.
        """
        return requests.get(f"{self.base_url}/smoothies")

# =============================================================================================================

    def get_all_ingredients(self):
        """
        Retrieves a list of all ingredients.
        :return: The server's response to the GET request.
        """
        return requests.get(f"{self.base_url}/ingredients")

# =============================================================================================================

    def update_smoothie_name(self, smoothie_id, smoothie_name):
        """
        Updates the name of an existing smoothie name.
        :param smoothie_id:
        :param smoothie_name:
        :return: The server's response to the PATCH request.
        """
        data_to_send = {
            "smoothie_name": smoothie_name
        }
        return requests.patch(f"{self.base_url}/smoothies/{smoothie_id}", json=data_to_send)

# =============================================================================================================

    def delete_smoothie(self, smoothie_id):
        """
        Deletes a smoothie by its id.
        :param smoothie_id:
        :return: The server's response to the DELETE request.
        """
        return requests.delete(f"{self.base_url}/smoothies/{smoothie_id}")

# =============================================================================================================

    def get_ingredients_by_id(self, ingredient_id):
        """
        Retrieves details for a specific ingredient by its id.
        :param ingredient_id:
        :return: The server's response to the GET request.
        """
        return requests.get(f"{self.base_url}/ingredients/{ingredient_id}")

# =============================================================================================================

    def create_new_ingredient(self, ingredient_name):
        """
        Creates a new ingredient api call to the back end.
        :param ingredient_name:
        :return: The server's response to the POST request.
        """
        ingredient = {"ingredient_name": ingredient_name}
        return requests.post(f"{self.base_url}/ingredients", json=ingredient)

# =============================================================================================================

    def update_ingredient(self, ingredient_id, ingredient_name, calories, protein, carbohydrates, sugar, fat):
        """
        Updates the details and nutritional facts of an existing ingredient.
        :param ingredient_id:
        :param ingredient_name:
        :param calories:
        :param protein:
        :param carbohydrates:
        :param sugar:
        :param fat:
        :return: The server's response to the PATCH request.
        """
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
        """
        Deletes a specific ingredient by its id.
        :param ingredient_id:
        :return: The server's response to the DELETE request.
        """
        return requests.delete(f"{self.base_url}/ingredients/{ingredient_id}")