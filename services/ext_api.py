import requests

def get_fruits_api(fruit):
    if not fruit: return "No fruit has been entered"
    fruit = fruit.capitalize().strip()

    BASE_URL = "https://www.fruityvice.com/api/fruit/all"

    response = requests.get(BASE_URL)
    fruits  = response.json()

    # pprint(fruits)
    # print(len(fruits))

    for i in range(len(fruits)):

        nutrition = fruits[i]["nutritions"]

        if fruit == fruits[i]["name"]:
            return  f"""
            ******************
            Fruit: {fruit}
            ******************
            Nutrition Summary (per 100g):
            Calories: {nutrition["calories"]}
            Fat: {nutrition["fat"]}
            Sugar: {nutrition["sugar"]}
            Carbs: {nutrition["carbohydrates"]}
            Protein: {nutrition["protein"]}
"""
    return "Cannot find this fruit. Try a different fruit or spelling."


print(get_fruits_api("banana"))