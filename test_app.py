import unittest
from app import app

class SmoothieIngredientsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_ingredients_route(self):
        response = self.app.get('/ingredients')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

if __name__ == '__main__':
    unittest.main()