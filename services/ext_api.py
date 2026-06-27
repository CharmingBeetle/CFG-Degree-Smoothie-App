import requests
from src.config import BASE_URL

def get_fruits_api(fruit):
    """
    Calls external Fruityvice API and when user inputs fruit name. Input cleaned and validated. Error handling if no
    connection or fruit does not exist.
    :param fruit:
    :return: Dictionary with fruit name and relevant nutrition data
    """

    if not isinstance(fruit, str): raise TypeError("Fruit entered should be a string.")
    fruit = fruit.capitalize().strip()
    if not fruit: raise ValueError("No fruit has been entered")

    try:
        response = requests.get(BASE_URL)
        fruits  = response.json()
    except requests.RequestException as error:
        raise ConnectionError(f"Could not connect to {BASE_URL}.", {error})

    ingredient_dict = {}

    for fruit_item in fruits:
        nutrition = fruit_item["nutritions"]

        if fruit == fruit_item["name"]:
            ingredient_dict["ingredient_name"] = fruit_item["name"]
            ingredient_dict["calories"] = nutrition["calories"]
            ingredient_dict["fat_g"] = nutrition["fat"]
            ingredient_dict["sugar_g"] = nutrition["sugar"]
            ingredient_dict["carbohydrates_g"] = nutrition["carbohydrates"]
            ingredient_dict["protein_g"] = nutrition["protein"]

            return ingredient_dict
    raise ValueError(f"Cannot find '{fruit_item}'. Try a different fruit or check spelling.")

