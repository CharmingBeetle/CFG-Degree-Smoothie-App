import unittest
from app import app

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

############### START  ##############################
#----------- POST /ingredients UNIT TESTS -----------------------------
    def test_add_ingredient_missing_request_body(self): # passed
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

    def test_add_ingredient_invalid_type(self): # passed
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

#------- POST /smoothies/<smoothie_id>/ingredients UNIT TESTS------------------
    def test_add_ingredient_to_smoothie_success(self): #passed
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

    def test_add_ingredient_to_smoothie_missing_fields(self): # passed
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

    def test_add_ingredient_to_smoothie_notfound_smoothie_id(self): #passed
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

    def test_add_ingredient_to_smoothie_notfound_ingredient_id(self): #passed
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

    def test_add_ingredient_to_smoothie_invalid_grams(self): # passed
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
#################### END ################################################


if __name__ == '__main__':
    unittest.main()

