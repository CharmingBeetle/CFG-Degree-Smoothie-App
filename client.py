from time import sleep
import sys

class SmoothieApp:
    def __init__(self):
        self.actions = {
            "1": self.view_all_smoothies,
            "2": self.search_smoothie_by_id,
            "3": self.add_new_smoothie,
            "4": self.update_smoothie,
            "5": self.delete_smoothie,
            "6": self.view_all_ingredients,
            "7": self.search_ingredient_by_id,
            "8": self.add_new_ingredient,
            "9": self.update_ingredient,
            "10": self.delete_ingredient,
            "11": self.exit_application
        }

    def welcome_message(self):
        print("""========================================================================================================
                🍑🍓🍇🥤 \x1B[4mWELCOME TO TERRY'S SMOOTHIE RECIPE MANAGEMENT API\x1B[0m 🥤🍇🍓🍑      
Where smoothie recipes are safely stored and updated, ingredients explored and nutrition data retrieved.
                           Press ENTER to open the menu and start blending...      
========================================================================================================""")
        input()
        line_1 = "Loading Menu....."
        line_2 = "Squeezing Fresh Juice....."
        line_3 = "Powering up Blenders....."
        line_4 = "Picking The Juiciest Strawberries.....\n"
        for x in line_1:
            print(x, end='')
            sys.stdout.flush()
            sleep(0.1)
        for x in line_2:
            print(x, end='')
            sys.stdout.flush()
            sleep(0.1)
        for x in line_3:
            print(x, end='')
            sys.stdout.flush()
            sleep(0.1)
        for x in line_4:
            print(x, end='')
            sys.stdout.flush()
            sleep(0.1)

    def show_menu(self):
        print("""\n\x1B[4mPlease choose an option:\x1B[0m
🥤[1] View All Smoothies
🍇[2] Search Smoothie by ID
🍓[3] Add a New Smoothie
🍑[4] Update a Smoothie
🗑️[5] Delete a Smoothie

📃[6] View All Ingredients
🍇[7] Search Ingredient by ID
🍓[8] Add New Ingredient
🍑[9] Update Ingredient
🗑️[10] Delete Ingredient
⬅️[11] Exit Application
""")
        return input("\n>>>")

    def run(self):
        self.welcome_message()

        while True:
            choice = self.show_menu()
            action = self.actions.get(choice)
            if action:
                action()
            else:
                print("Invalid option. Please choose 1-8.")

    def view_all_smoothies(self):
     print("Loading...")

    def search_smoothie_by_id(self):
     print("Loading...")

    def add_new_smoothie(self):
     print("Loading...")

    def update_smoothie(self):
     print("Loading...")

    def delete_smoothie(self):
     print("Loading...")

    def view_all_ingredients(self):
     print("Loading...")

    def search_ingredient_by_id(self):
     print("Loading...")

    def add_new_ingredient(self):
     print("Loading...")

    def update_ingredient(self):
     print("Loading...")

    def delete_ingredient(self):
     print("Loading...")

    def exit_application(self):
     print("Loading...")

if __name__ == "__main__":
   app = SmoothieApp()
   app.run()
