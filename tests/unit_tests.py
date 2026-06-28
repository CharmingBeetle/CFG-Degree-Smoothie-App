import unittest
from app import app
import sys
import os

project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, project_root)



class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()


# ------------------------    GET /ingredients     ------------------------------

    def test_get_ingredients_success(self):
        """
        Should return 200 when retrieving all ingredients from database
        :return: 200
        """
        response = self.client.get('/ingredients')
        self.assertEqual(response.status_code, 200)

#------------------------------ POST /ingredients  -----------------------------
    def test_add_ingredient_missing_request_body(self):
        """
        No request body should return 400
        :return:400
        """

        response = self.client.post(
            '/ingredients',
            json={}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_add_ingredient_invalid_type(self):
        """
        Should return 400 if ingredient_name not a string
        :return: 400
        """
        response = self.client.post(
            '/ingredients',
            json={"ingredient_name": 7}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_add_ingredient_not_found_in_api(self):
        """
        Fruit not found in Fruityvice API should return 404
        :return: 404
        """
        response = self.client.post(
            '/ingredients',
            json={"ingredient_name": "Burberry"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

#---------------    POST /smoothies/<smoothie_id>/ingredients    -----------------
    def test_add_ingredient_to_smoothie_success(self):
        """
        Should return 201 if added successfully to smoothie
        :return: 201
        """
        response = self.client.post(
            '/smoothies/1/ingredients',
            json={
                "ingredient_id" : 1,
                "grams" : 300
        }
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.get_json())

    def test_add_ingredient_to_smoothie_missing_fields(self):
        """
        Should return 400 if empty request body
        :return: 400
        """
        response = self.client.post(
            '/smoothies/1/ingredients',
            json={}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_add_ingredient_to_smoothie_notfound_smoothie_id(self):
        """
        Should return 404 if smoothie ID not found in DB
        :return: 404
        """
        response = self.client.post(
                '/smoothies/9999999/ingredients',
                json={
        'ingredient_id': '3',
        'grams' : '300'
    }
            )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    def test_add_ingredient_to_smoothie_notfound_ingredient_id(self):
        """
        Should return 404 if ingredient_id not found
        :return: 404
        """
        response = self.client.post(
            '/smoothies/1/ingredients',
            json={
                'ingredient_id' : 9999999,
                'grams' : 300
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    def test_add_ingredient_to_smoothie_invalid_grams(self):
        """
        Should return 400 if ingredient_id invalid
        :return: 400
        """
        response = self.client.post(
            '/smoothies/1/ingredients',
            json={
                'ingredient_id' : 1,
                'grams' : 0
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())


# ----------------  PATCH /smoothies/<smoothie_id>  -----------------------------------

    def test_update_smoothie_success(self):
        """
        Should return 200 if smoothie updated successfully
        :return: 200
        """

        response = self.client.patch(
                '/smoothies/1',
                json={
                "smoothie_name": "Berry Blast"
                }
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

# -----------------  PATCH /ingredients/<ingredient_id> -------------------------------

    def test_update_ingredient_success(self):
        """
        Should return 200 if ingredient updated successfully
        :return:200 
        """
        response = self.client.patch(
            '/ingredients/1',
            json={
            "ingredient_name": "Apple",
            "calories": 99,
            "protein_g": 0.3,
            "carbohydrates_g": 13.8,
            "sugar_g": 10.4,
            "fat_g": 0.2
                }
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

# --------------     DELETE /smoothies/<smoothie_id> ---------------------------------









# -----------------------------   END -------------------------------------------------










if __name__ == '__main__':
    unittest.main()