# 🥤 Terry's Smoothie Recipe Management API 🍓🍑🍌

Hello All! This is a Flask-based REST API for managing smoothie recipes and ingredients, with nutrition data fetched from the Fruityvice external API. Includes a terminal client so the user can interact with the app. As the user of the app you will be able to create new smoothie recipes, search for new ingredients to add to the recipe book (database) along with their nutritional values, add new ingredients to individual smoothie recipes, update or delete existing ingredients in a smoothie and delete a smoothie recipe.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Database Setup](#database-setup)
- [How to Run the App](#how-to-run-the-app)
- [API Endpoints](#smoothie-app-api-endpoints)
- [Running Tests](#running-tests)
- [File Architecture](#file-architecture)
- [Contributors](#contributors)

---

## Project Overview

This app allows users to:

- View, create, update, and delete smoothie recipes
- View, add, update, and delete ingredients
- Fetch nutrition data for new ingredients automatically via the external Fruityvice API
- Use a terminal-based client UI to interact with the system

---

## Tech Stack

- **Python 3 / Flask** — API server
- **MySQL** — relational database
- **mysql-connector-python** — database driver
- **Requests** — HTTP client for external API calls
- **Fruityvice API** — external nutrition data source (`https://www.fruityvice.com/api/fruit/all`)
- **unittest** — testing framework used

---

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the database connection** in `config.py`:
   ```python
   db_config = {
       "host": "localhost",
       "user": "root",
       "password": "<your_mysql_password>",
       "database": "smoothie_ingredients_db"
   }
   ```
---

## Database Setup

Run the provided SQL script to create and seed the database:

```bash
mysql -u root -p < smoothie_ingredients_db.sql
```

This will create three tables: `smoothies`, `ingredients`, and `smoothie_ingredients`, and populate them with initial data.

---

## How to Run the App

**1. Start the Flask API server:**
```bash
python app.py
```
The server runs on `http://127.0.0.1:5000` by default.

**2. Launch the terminal client:**
```bash
python client.py
```

---

## Smoothie App API Endpoints

### Smoothies

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/smoothies` | Get all smoothies |
| GET | `/smoothies/<smoothie_id>` | Get a smoothie by ID |
| POST | `/smoothie` | Add a new smoothie |
| PATCH | `/smoothies/<smoothie_id>` | Update a smoothie name |
| DELETE | `/smoothies/<smoothie_id>` | Delete a smoothie |

### Ingredients

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ingredients` | Get all ingredients |
| GET | `/ingredients/<ingredient_id>` | Get an ingredient by ID |
| POST | `/ingredients` | Add a new ingredient (fetches nutrition from Fruityvice) |
| PATCH | `/ingredients/<ingredient_id>` | Update ingredient calories |
| DELETE | `/ingredients/<ingredient_id>` | Delete an ingredient |

### Smoothie Ingredients

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/smoothies/<smoothie_id>/ingredients` | Add an ingredient to a smoothie |

---

### Example: GET `/smoothies/<smoothie_id>`

```json
{
  "method": "GET",
  "route": "/smoothies/<smoothie_id>",
  "description": "Returns a single smoothie by ID",
  "request_body": null,
  "example_request": "GET /smoothies/1",
  "example_response": {
    "status": 200,
    "body": {
      "smoothie_id": 1,
      "smoothie_name": "Append and Blend"
    }
  },
  "error_responses": {
    "404": { "error": "Smoothie not found" }
  }
}
```

### Example: POST `/ingredients`

```json
{
  "method": "POST",
  "route": "/ingredients",
  "description": "Searches the Fruityvice external API by fruit name, retrieves nutrition data (calories, protein, carbohydrates, sugar, fat per 100g) and saves the full ingredient record to the ingredients table in the database",
  "request_body": {
    "fruit_name": "string (required)"
  },
  "example_request": {
    "fruit_name": "banana"
  },
  "example_response": {
    "status": 201,
    "body": {
      "ingredient_id": 12,
      "ingredient_name": "Banana",
      "calories": 96.0,
      "protein_g": 1.0,
      "carbohydrates_g": 22.0,
      "sugar_g": 17.2,
      "fat_g": 0.2,
      "message": "Banana added successfully"
    }
  },
  "error_responses": {
    "400": { "error": "Please provide a fruit_name" },
    "404": { "error": "Cannot find 'Dragonfruit'. Try a different fruit or check spelling." },
    "503": { "error": "Could not connect to API" },
    "500": { "error": "Failed to add ingredient" }
  }
}
```

---

## Running Tests

Three types of testing have been implemented:

1. **Unit Tests** covering most of the functions (`tests/unit_tests.py`)
2. **Manual Testing** via Postman screenshots (`tests/manual_tests/`)
3. **Smoke Tests** covering some `db_utils` functions and helper functions (`tests/smoke_tests.py`)

To run unit tests: 
```bash
python -m unittest unit_tests.py -v
```

Tests cover:

- `POST /ingredients` — missing body, invalid type, fruit not found in Fruityvice
- `POST /smoothies/<smoothie_id>/ingredients` — success, missing fields, invalid smoothie/ingredient IDs, invalid grams
- *(insert further tests here)*

> **Note:** The 201 success case for `POST /ingredients` is checked manually via Postman (see screenshots in `tests/manual_tests/`).

---

## File Architecture

```
.
├── src/
│   ├── app.py                          # Flask routes
│   ├── client.py                       # Terminal client UI
│   ├── config.py                       # DB and API config
│   └── db_utils.py                     # Database helper functions
├── models/
│   └── nutrition.py                    # External API class
├── services/
│   └── ext_api.py                      # Fruityvice API integration
├── database/
│   └── smoothie_ingredients_db.sql     # Database schema and seed data
├── tests/
│   ├── unit_tests.py                   # Unit tests
│   ├── manual_tests/                   # Request/Response screenshots using Postman
│   └── smoke_tests.py                  # Smoke tests for db_utils functions
└── requirements.txt                    # Modules and packages required
└── .gitignore
```

---

## Contributors

> Update your contributions below!

| Name | Contributions                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Aisha | **GET ingredients** (app.py); `<insert_function_name>`, `<insert_function_name>` (db_utils), (config.py)                                                                                                                                                                                                                                                                                                                                                                     |
| Charlotte | **POST + DELETE smoothie routes** (app.py), `add_smoothie_db` (db_utils), (client.py)                                                                                                                                                                                                                                                                                                                                                                                        |
| Lara | **PATCH smoothie routes** (app.py); `get_all_smoothies`, `get_smoothie_by_id` (db_utils)                                                                                                                                                                                                                                                                                                                                                                                     |
| Elle | **DELETE ingredient routes** (app.py); `<insert_function_name>`, `<insert_function_name>` (db_utils)                                                                                                                                                                                                                                                                                                                                                                         |
| Nina | **POST ingredient routes** (app.py); `add_ingredient_db`, `add_ingredient_to_smoothie_db`, helper functions: (get ingredient and smoothie names/ smoothie exisits/ ingredient exists) (db_utils); class `Nutritionist` (nutrition.py); tests `POST /ingredient` + `POST /smoothies/<smoothie_id>/ingredients` (unit_tests.py); db_utils functions + helper functions (smoke_tests.py); manual testing POST ingredients (tests/manual_tests); (requirements.txt); (README.md) |
| Teresa | **GET smoothie + GET ingredient routes** (app.py); `get_all_smoothies`, `get_smoothie_by_id` (db_utils)                                                                                                                                                                                                                                                                                                                                                                      |

---

> **Note:** This README is a first draft — details to be updated 