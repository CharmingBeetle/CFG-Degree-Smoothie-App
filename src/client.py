from config import API_URL
from tabulate import tabulate
from colorama import init, Fore, Style
from src.api_client import APIClient

init()

#=============================================================================================================

class SmoothieApp:
    def __init__(self):
        self.api = APIClient(API_URL)
        self.actions = {
            "1": self.get_all_smoothies_front_end,
            "2": self.get_smoothie_by_id_front_end,
            "3": self.create_new_smoothie_front_end,
            "4": self.update_smoothie_front_end,
            "5": self.delete_smoothie_front_end,
            "6": self.get_all_ingredients_front_end,
            "7": self.get_ingredients_by_id_front_end,
            "8": self.create_new_ingredient_front_end,
            "9": self.update_ingredient_front_end,
            "10": self.delete_ingredient_front_end,
            "11": self.add_new_ingredient_to_smoothie_front_end,
            "12": self.exit_application_front_end
        }

# =============================================================================================================

    def welcome_message(self):
        """
        Displays welcome message and waits for user input 'Enter' to continue.
        :return: None.
        """
        print(f"""========================================================================================================
                🍑🍓🍇🥤 {Style.BRIGHT}{Fore.CYAN}WELCOME TO THE SMOOTHIE RECIPE MANAGEMENT API{Style.RESET_ALL} 🥤🍇🍓🍑      
Where smoothie recipes are safely stored and updated, ingredients explored and nutrition data retrieved.
                           Press ENTER to open the menu and start blending...      
========================================================================================================""")
        input()

# =============================================================================================================

    def show_menu(self):
        """
        Displays the menu and captures client's choice.
        :return: Menu choice.
        """
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

🥤[11] Customise your smoothie

⬅️[12] Exit Application
""")
        return input(">>>")

    def run(self):
        """
        Main application lifecycle.
        :return: None.
        """
        self.welcome_message()
        self.menu()

    def menu(self):
        """
        Displays the application's main menu, processes the client's input and recursively loops.
        :return: None.
        """
        choice = self.show_menu()
        action = self.actions.get(choice)

        if action:
            action()
        else:
            print("Invalid option. Please choose 1-12.")

        self.menu()

# =============================================================================================================

    def get_all_smoothies_front_end(self):
        """
        Retrieves all smoothies from the API and displays them.
        :return: A list of dictionaries containing smoothie data.
        """
        smoothies = self.api.get_all_smoothies().json()

        ordered_smoothies_list = [[
                smoothie["smoothie_id"],
                smoothie["name"],
                smoothie["ingredients"]]
        for smoothie in smoothies]

        print(tabulate(ordered_smoothies_list, headers=["Smoothie ID", "Name", "Ingredients (grams)"],
                       tablefmt="grid"))

        return smoothies

# =============================================================================================================

    def get_smoothie_by_id_front_end(self):
        """
        Prompts client for a smoothie id and displays the client's smoothie choice.
        :return: None.
        """
        smoothie_id = None

        while True:
            try:
                smoothie_id = int(input("Enter smoothie ID: "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

        response = self.api.get_smoothie_by_id(smoothie_id)
        if response.status_code == 200:
            smoothie = response.json()

            row = [[
                smoothie["smoothie_id"],
                smoothie["name"]]
            ]

            print(tabulate(row, headers=["Smoothie ID", "Name"], tablefmt="grid"))

        else:
            print(response.json()["error"])

# =============================================================================================================

    def create_new_smoothie_front_end(self):
        """
        Creates a new smoothie from gathering a name from the client.
        :return: None.
        """
        smoothie_name = input("Enter smoothie name: ").strip()

        response = self.api.create_new_smoothie(smoothie_name)

        if response.status_code == 201:
            data = response.json()
            print(f"{data['message']}")
            print(f"Smoothie ID: {data['smoothie_id']}")

        else:
            data = response.json()
            print(f"error: {data['error']}")

# =============================================================================================================

    def add_new_ingredient_to_smoothie_front_end(self):
        """
        Guides the client through an interactive loop to customise their smoothie.
        :return: None
        """
        available_smoothies = self.get_all_smoothies_front_end()
        selected_smoothie_id = None
        MAX_GRAMS = 9999.99

        while True:
            try:
                selected_smoothie_id = int(input("Please enter the ID of the smoothie you would like to customise: "))
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

            if any(smoothie["smoothie_id"] == selected_smoothie_id for smoothie in available_smoothies):
                break

            print("Smoothie ID not found. Please try again.\n")

        available_ingredients = self.get_all_ingredients_front_end()

        while True:
            try:
                ingredient_id_input = input("Please enter the ID of the ingredient you would like to add (or press 'q' to quit): ")

                if ingredient_id_input.lower() == "q":
                    break

                selected_ingredient_id = int(ingredient_id_input)

                if not any(ingredient["ingredient_id"] == selected_ingredient_id for ingredient in available_ingredients):
                    print("Ingredient ID not found. Please try again.\n")
                    continue

                grams_input = input("Please enter the amount in grams that you would like to add: ")

                ingredient_grams = float(grams_input)

                if ingredient_grams > MAX_GRAMS:
                    print(f"That amount is too high (less than {MAX_GRAMS}), please try again.")
                    continue

                response = self.api.add_ingredient_to_smoothie(selected_smoothie_id, selected_ingredient_id, ingredient_grams)

                response_date = response.json()

                if response.status_code == 201:
                    print(response_date["message"])
                else:
                    print(f"error: {response_date['error']}")

            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

# =============================================================================================================

    def update_smoothie_front_end(self):
        """
        Updates the name of an existing smoothie.
        :return: None.
        """
        smoothies = self.get_all_smoothies_front_end()
        user_id_choice = None

        while True:
            try:
                user_id_choice = int(input("Please enter the ID of the smoothie you would like to update: "))
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

            if any(smoothie["smoothie_id"] == user_id_choice for smoothie in smoothies):
                break

            print("Smoothie ID not found. Please try again.\n")

        user_new_name_choice = input("Please enter new smoothie name: ").strip()

        response = self.api.update_smoothie_name(user_id_choice, user_new_name_choice)

        if response.status_code == 200:
            data = response.json()
            print(f"Smoothie ID: {data['smoothie_id']} name updated to {data['new_name']}")
        else:
            data = response.json()
            print(f"error: {data['error']}")

# =============================================================================================================

    def delete_smoothie_front_end(self):
        """
        Validates and deletes a smoothie via client prompt.
        :return: None.
        """
        smoothies = self.get_all_smoothies_front_end()
        choice = None

        while True:
            try:
                choice = int(input("Please enter the ID of the smoothie you would like to delete: "))
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

            if any(smoothie["smoothie_id"] == choice for smoothie in smoothies):
                break

            print("Smoothie ID not found. Please try again.\n")

        response = self.api.delete_smoothie(choice)

        if response.status_code == 200:
            print(response.json()["message"])
        else:
            print(f"Error: {response.json()['error']}")

# =============================================================================================================

    def get_all_ingredients_front_end(self):
        """
        Fetches all nutritional values and formats them into a table.
        :return: A list of dictionaries representing the ingredients inventory.
        """
        ingredients = self.api.get_all_ingredients().json()

        ordered_ingredients_list = [[
                ingredient["ingredient_id"],
                ingredient["ingredient_name"],
                ingredient["calories"],
                ingredient["fat_g"],
                ingredient["sugar_g"],
                ingredient["carbohydrates_g"],
                ingredient["protein_g"]
        ]
            for ingredient in ingredients]

        print(tabulate(ordered_ingredients_list, headers=["Ingredient ID", "Name", "Calories", "Fat", "Sugar", "Carbohydrates", "Protein"],
                       tablefmt="grid"))

        return ingredients

# =============================================================================================================

    def get_ingredients_by_id_front_end(self):
        """
        Requests and presents name attributes of an individual ingredient matching the id.
        :return: None.
        """
        ingredient_id = None

        while True:
            try:
                ingredient_id = int(input("Enter ingredient ID: "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

        response = self.api.get_ingredients_by_id(ingredient_id)
        if response.status_code == 200:
            ingredient = response.json()

            row = [[
                ingredient["ingredient_id"],
                ingredient["ingredient_name"]]]

            print(tabulate(row, headers=["Ingredient ID", "Name"], tablefmt="grid"))

        else:
            print(response.json()["error"])

# =============================================================================================================

    def create_new_ingredient_front_end(self):
        """
        Creates a new ingredient from gathering a name from the client.
        :return: None.
        """
        ingredient_name = input("Enter ingredient name: ").strip()

        response = self.api.create_new_ingredient(ingredient_name)

        if response.status_code == 201:
            data = response.json()
            print(f"{data['message']}")
            print(f"Ingredient ID: {data['ingredient_id']}")

        else:
            data = response.json()
            print(f"error: {data['error']}")

# =============================================================================================================

    def update_ingredient_front_end(self):
        """
        Updates the name of an existing ingredient.
        :return: None.
        """
        ingredients = self.get_all_ingredients_front_end()
        user_id_choice = None
        user_new_name_choice = None
        user_calorie_choice = None
        user_protein_choice = None
        user_carbohydrates_choice = None
        user_sugar_choice = None
        user_fat_choice = None

        while True:
            try:
                user_id_choice = int(input("Please enter the ID of the ingredient you would like to update: "))
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

            if any(ingredient["ingredient_id"] == user_id_choice for ingredient in ingredients):
                break

            print("Ingredient ID not found. Please try again.\n")

        while True:
            user_new_name_choice = input("Please enter new ingredient name: ")
            if not user_new_name_choice.replace(" ", "").isalpha():
                print("Invalid input. Please enter alphabetical characters.\n")
                continue
            break

        while True:
            try:
                user_calorie_choice = float(input("Please enter total amount of calories: "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

        while True:
            try:
                user_protein_choice = float(input("Please enter total amount of protein (grams): "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

        while True:
            try:
                user_carbohydrates_choice = float(input("Please enter total amount of carbohydrates (grams): "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

        while True:
            try:
                user_sugar_choice = float(input("Please enter total amount of sugar (grams): "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

        while True:
            try:
                user_fat_choice = float(input("Please enter total amount of fat (grams): "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

        response = self.api.update_ingredient(user_id_choice, user_new_name_choice, user_calorie_choice, user_protein_choice, user_carbohydrates_choice, user_sugar_choice, user_fat_choice)

        if response.status_code == 200:
            data = response.json()
            print(f"Ingredient ID: {data['ingredient_id']} has been updated.")
        else:
            data = response.json()
            print(f"error: {data['error']}")

# =============================================================================================================

    def delete_ingredient_front_end(self):
        """
        Validates and deletes an ingredient via client prompt.
        :return: None.
        """
        ingredients = self.get_all_ingredients_front_end()
        choice = None

        while True:
            try:
                choice = int(input("Please enter the ID of the ingredient you would like to delete: "))
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

            if any(ingredient["ingredient_id"] == choice for ingredient in ingredients):
                break

            print("Ingredient ID not found. Please try again.\n")

        response = self.api.delete_ingredient(choice)

        if response.status_code == 200:
            print(response.json()["message"])
        else:
            print(f"Error: {response.json()['error']}")

# =============================================================================================================

    def exit_application_front_end(self):
        """
        Exits program execution and prints a goodbye message.
        :return: None.
        """
        print("Goodbye!")
        exit()

#=============================================================================================================

if __name__ == "__main__":
   app = SmoothieApp()
   app.run()
