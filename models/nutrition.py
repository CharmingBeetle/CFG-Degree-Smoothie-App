from services.ext_api import get_fruits_api

class Nutritionist:

    @staticmethod
    def search_ingredient(fruit_name):
        """
        Uses the fruit_name variable in the get_fruits_api call
        :param fruit_name:
        :return: Returns a dict with named fruit and nutrition data
        """
        return get_fruits_api(fruit_name)


nutrition_api = Nutritionist()
