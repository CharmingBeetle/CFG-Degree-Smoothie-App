import unittest
import importlib.util
import sys
import os

# 1. Force find the exact local app.py file next to this test file
local_app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")

spec = importlib.util.spec_from_file_location("app", local_app_path)
app_module = importlib.util.module_from_spec(spec)
sys.modules["app"] = app_module
spec.loader.exec_module(app_module)

from app import app

class SmoothieIngredientsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_ingredients_route(self):
        # We simulate sending a real ingredient payload to the POST route
        test_ingredient = {
            "ingredient_name": "Cherry",
            "calories": 50,
            "fat_g": 0.3,
            "sugar_g": 8.0,
            "carbohydrates_g": 12.0,
            "protein_g": 1.0
        }
        response = self.app.post('/ingredients', json=test_ingredient)
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()


    def test_get_ingredients_success(self):
        response = self.app.get('/ingredients')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(type(data), list)