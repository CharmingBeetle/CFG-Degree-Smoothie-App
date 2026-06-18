import unittest
from app import app
# from db_utils import delete_smoothie_ingredient_db
# run 'python -m unittest tests/test_smoothie_app.py -v' in terminal to see which tests passed and failed

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # def tearDown(self):
    #     """Remove test data inserted during tests"""
    #     from db_utils import delete_smoothie_ingredient_db
    #     delete_smoothie_ingredient_db(smoothie_id=1, ingredient_id=1)

############### START  ##############################
# Nina: LINES 16 - 43
# * Tear down func commented out to refresh when new item added *
#----------- POST /ingredients UNIT TESTS -----------------------------
#
# 201 for successful entry tested via manual testing/screenshots on Postman
# unit test for this would require mocking and interaction with DB
#

    def test_add_ingredient_missing_request_body(self): # passed
        """No request body should return 400 """
        response = self.client.post(
            '/ingredients',
            json={}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_add_ingredient_invalid_type(self): # passed
        """Should return 400 if ingredient_name not a string"""
        response = self.client.post(
            '/ingredients',
            json={"ingredient_name": 7}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_add_ingredient_not_found_in_api(self):
        """Fruit not found in Fruityvice API should return 404"""
        response = self.client.post(
            '/ingredients',
            json={"ingredient_name": "Burberry"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())


if __name__ == '__main__':
    unittest.main()

