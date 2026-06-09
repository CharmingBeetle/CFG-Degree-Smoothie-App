import requests
from pprint import pprint
from config import BASE_URL

def get_fruits_api(fruit):
    if type(fruit) != str: return "Fruit should be a string."
    if not fruit: return "No fruit has been entered"
    fruit = fruit.capitalize().strip()

    response = requests.get(BASE_URL)
    fruits  = response.json()

    ingredient_dict = {}
    for i in range(len(fruits)):
        nutrition = fruits[i]["nutritions"]

        if fruit == fruits[i]["name"]:
            ingredient_dict["fruit_name"] = fruits[i]["name"]
            ingredient_dict["calories_100g"] = nutrition["calories"]
            ingredient_dict["fat_100g"] = nutrition["fat"]
            ingredient_dict["sugar_100g"] = nutrition["sugar"]
            ingredient_dict["carbs_100g"] = nutrition["carbohydrates"]
            ingredient_dict["protein_100g"] = nutrition["protein"]

            return ingredient_dict

    return "Cannot find this fruit. Try a different fruit or spelling."


pprint(get_fruits_api("banana"), sort_dicts=False)