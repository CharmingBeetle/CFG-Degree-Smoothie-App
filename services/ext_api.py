import requests
from pprint import pprint
from config import BASE_URL

def get_fruits_api(fruit):

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
            ingredient_dict["fruit_name"] = fruit_item["name"]
            ingredient_dict["calories_100g"] = nutrition["calories"]
            ingredient_dict["fat_100g"] = nutrition["fat"]
            ingredient_dict["sugar_100g"] = nutrition["sugar"]
            ingredient_dict["carbs_100g"] = nutrition["carbohydrates"]
            ingredient_dict["protein_100g"] = nutrition["protein"]

            return ingredient_dict
    raise ValueError(f"Cannot find '{fruit_item}'. Try a different fruit or check spelling.")

pprint(get_fruits_api("cherry"), sort_dicts=False)