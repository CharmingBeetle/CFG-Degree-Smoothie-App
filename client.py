import sys
import requests
from time import sleep
from config import API_URL
from tabulate import tabulate
from colorama import init, Fore, Style
init()

#=============================================================================================================

def typewriter_effect(lines, delay=0.1):
    """
    Print each line character by character to create a typewriter 'loading' effect.
    :param lines:
    :param delay:
    :return: A list of strings.
    """
    for line in lines:
        for char in line:
            print(char, end="")
            sys.stdout.flush()
            sleep(delay)
        print()

#=============================================================================================================

class SmoothieApp:
    def __init__(self):
        self.actions = {
            "1": self.get_all_smoothies_front_end,
            "2": self.get_smoothie_by_id_front_end,
            "3": self.add_new_smoothie,
            "4": self.update_smoothie,
            "5": self.delete_smoothie,
            "6": self.get_ingredients_front_end,
            "7": self.search_ingredient_by_id,
            "8": self.add_new_ingredient,
            "9": self.update_ingredient,
            "10": self.delete_ingredient,
            "11": self.exit_application
        }

# =============================================================================================================

    def welcome_message(self):
        print(f"""========================================================================================================
                🍑🍓🍇🥤 {Style.BRIGHT}{Fore.CYAN}WELCOME TO THE SMOOTHIE RECIPE MANAGEMENT API{Style.RESET_ALL} 🥤🍇🍓🍑      
Where smoothie recipes are safely stored and updated, ingredients explored and nutrition data retrieved.
                           Press ENTER to open the menu and start blending...      
========================================================================================================""")
        # input()
        #
        # lines = [
        #     "Loading Menu.....",
        #     "Squeezing Fresh Juice.....",
        #     "Powering up Blenders.....",
        #     "Picking The Juiciest Strawberries...\n"
        # ]
        #
        # typewriter_effect(lines)

# =============================================================================================================

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
        return input(">>>")

    def run(self):
        self.welcome_message()

        while True:
            choice = self.show_menu()
            action = self.actions.get(choice)
            if action:
                action()
            else:
                print("Invalid option. Please choose 1-11.")

# =============================================================================================================

    def get_all_smoothies_front_end(self):
        smoothies = requests.get(API_URL + "/smoothies").json()
        ordered_smoothies_list = [
            [
                smoothie["smoothie_id"],
                smoothie["name"],
                smoothie["ingredients"]
            ]
        for smoothie in smoothies
        ]
        print(tabulate(ordered_smoothies_list, headers=["Smoothie ID", "Name", "Ingredients (grams)"],
                       tablefmt="grid"))
        input("\nPress Enter to return to the menu...")

# =============================================================================================================

    def get_smoothie_by_id_front_end(self):
        smoothie_id = input("Enter smoothie ID: ")

        response = requests.get(f"{API_URL}/smoothies/{smoothie_id}")
        if response.status_code == 200:
            smoothie = response.json()

            row = [[
                smoothie["smoothie_id"],
                smoothie["name"]]]

            print(tabulate(row, headers=["Smoothie ID", "Name"], tablefmt="grid"))

        else:
            print(response.json()["error"])

        input("\nPress Enter to return to the menu...")

# =============================================================================================================

    def add_new_smoothie(self):
        print("Loading...")

    def update_smoothie(self):
        print("Loading...")

    def delete_smoothie(self):
        print("Loading...")

# =============================================================================================================

    def get_ingredients_front_end(self):
        ingredients = requests.get(API_URL + "/ingredients").json()
        ordered_ingredients_list = [
            [
                ingredient["ingredient_id"],
                ingredient["ingredient_name"]
            ]
            for ingredient in ingredients
        ]
        print(tabulate(ordered_ingredients_list, headers=["Ingredient ID", "Name"],
                       tablefmt="grid"))
        input("\nPress Enter to return to the menu...")

# =============================================================================================================

    def get_ingredients_by_id_front_end(self):
        print("Loading...")

# =============================================================================================================


    def add_new_ingredient(self):
        print("Loading...")

    def update_ingredient(self):
        print("Loading...")

    def delete_ingredient(self):
        print("Loading...")

    def exit_application(self):
        print("Goodbye!")
        exit()

#=============================================================================================================

if __name__ == "__main__":
   app = SmoothieApp()
   app.run()
