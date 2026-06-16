# nutrition class
from services.ext_api import get_fruits_api

class Nutritionist:

    def __init__(self, fruit_name):
        self.fruit_name = fruit_name

    # class methods
    def search_ingredient(self, fruit_name):
        #call food api and receive data
        return get_fruits_api(fruit_name)


nutrition_api = Nutritionist("banana")


