from src.app import ingredient_db, smoothie_db, smoothie_ingredient_db

def run_smoke_tests():
    """
    This tests assertions for db_utils for 'POST ingredients' adding new ingredients /
    to database and helper functions.
    * Note: database must be manually re-seeded after each run.
    :return: Ingredient ID / New smoothie name created / Success if all tests have passed
    """""

    test_ingredient = {
    'ingredient_name': 'Testberry',
    'calories': 30,
    'protein_g': 20.0,
    'carbohydrates_g': 5.4,
    'sugar_g': 3.4,
    'fat_g': 0.4
}

    ingredient_id = ingredient_db.create_new_ingredient_db(test_ingredient)
    test_smoothie_id = smoothie_db.create_new_smoothie_db({"smoothie_name" : "Test&Lime"})

    assert ingredient_id is not None
    assert ingredient_db.helper_ingredient_exists_by_id_db(ingredient_id)
    assert smoothie_db.helper_smoothie_exists_by_id_db(test_smoothie_id)

    smoothie_ingredient_row_id = smoothie_ingredient_db.add_new_ingredient_to_smoothie_db(test_smoothie_id,ingredient_id,200)
    assert smoothie_ingredient_row_id is not None

    smoothie_name, ingredient_name = smoothie_ingredient_db.helper_get_smoothie_and_ingredient_name_db(test_smoothie_id, ingredient_id)
    assert smoothie_name == 'Test&Lime'
    assert ingredient_name == "Testberry"


if __name__ == "__main__":
    run_smoke_tests()
    print("Smoke testing passed! 🎉")