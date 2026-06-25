from db_utils import (
    add_new_smoothie_db,
    add_ingredient_db,
    add_ingredient_to_smoothie_db,
    helper_smoothie_exists,
    helper_ingredient_exists,
    helper_get_smoothie_and_ingredient_names
)
### ***** POST SMOOTHIE REQUIRES REFACTORING FOR SMOKE TESTS TO PASS **** #####

def run_smoke_tests():
# add code here or at the bottom
# do not merge to main if tests to not pass!
#================================================================
# NINA: Smoke tests POST /ingredients, /smoothies/id/ingredients
#------------- START -----------------------------------
    test_ingredient = {
    'ingredient_name': 'Testberry',
    'calories': 30,
    'protein_g': 20.0,
    'carbohydrates_g': 5.4,
    'sugar_g': 3.4,
    'fat_g': 0.4
}
    # insert the new ingredient and get the id
    ingredient_id = add_ingredient_db(test_ingredient)
    test_smoothie_id = add_new_smoothie_db({"name" : "Test&Lime"})

    # assertions
    assert ingredient_id is not None
    assert helper_ingredient_exists(ingredient_id)
    assert helper_smoothie_exists(test_smoothie_id)

    smoothie_ingredient_row_id = add_ingredient_to_smoothie_db(test_smoothie_id,ingredient_id,200)
    assert smoothie_ingredient_row_id is not None

    smoothie_name, ingredient_name = helper_get_smoothie_and_ingredient_names(test_smoothie_id, ingredient_id)
    assert smoothie_name == 'Test&Lime'
    assert ingredient_name == "Testberry"
#----------------- END ---------------------------------------
# or add code here


if __name__ == "__main__":
    run_smoke_tests()
    # reset_db() ==> can add reset db here manually or with function (if time allows)
    print("Smoke testing passed! 🎉")