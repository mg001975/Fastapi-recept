# FastAPI Recipe Project

## Overview

This is a FastAPI project for managing and importing recipes from YAML files into an SQLite database. The recipes are structured with components, steps, and ingredients, and are inserted into a relational database. This project is useful for managing culinary recipes and processing them programmatically.

## Project Structure

```
.
├── app.py                # FastAPI main application
├── database              # Folder containing database-related files
│   ├── database.py       # Database configuration and connection setup
│   ├── models.py         # Database models (Recipe, Component, Step, Ingredient)
│   ├── schemas.py        # Database pydantic schema (Recipe, Component, Step, Ingredient)
├── recipes.db            # SQLite database
├── imports               # Folder to store your YAML recipe files
├── routers               # FastAPI routers
├── static                # Static assets (CSS, JS, etc.)
├── templates             # HTML templates
├── utils                 # HTML templates
└── readme.md             # This file
```

## Requirements

Before running the project, you need to install the required dependencies. Create a virtual environment and install dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Ensure that you have the following packages installed:

- fastapi
- uvicorn
- sqlalchemy
- pydantic
- pyyaml
- sqlite

## Database Configuration

The SQLite database is used to store recipes, components, steps, and ingredients. By default, the database file (`recipes.db`) is stored in the root of the project directory.

- Database models: Located in models.py
- Database configuration: Located in database.py
- Database schema: Located in schemas.py


## Running the Application

To run the FastAPI application, use the following command:

```bash
# Run the app 
python app.py
```

Visit the application in your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Importing Recipes from YAML

This project includes a script that allows you to import recipe data from YAML files into the database. Follow these steps to import your recipes:

1. **Prepare your YAML Files**: Make sure your recipes are structured as YAML files.

### Format of the YAML Files

Example of a valid YAML structure:

```yaml
- name: Recept hoofddeeg direct
  category: Pizza
  description: hoofddeeg directe methode
  prep_time: 15
  difficulty: easy
  RecipeComponent:
    - component_name: Hoofddeeg
      component_description: Hoofdeeg kneden, 7 bollen a 230 gram
      Steps:
        - step_description: deeg maken
      Ingredients:
        - ingredient_name: bloem
          ingredient_amount: 1000
          ingredient_unit: gram
        - ingredient_name: water
          ingredient_amount: 600
          ingredient_unit: gram
        - ingredient_name: gist
          ingredient_amount: 3
          ingredient_unit: gram
        - ingredient_name: zout
          ingredient_amount: 15
          ingredient_unit: gram
```
## Exporting Recipes from YAML

Backup youre recipes to a yaml file.

3. **Check the Database**:

Once the import is complete, check the recipes.db SQLite database to ensure the recipes are inserted correctly. You can use a database viewer like DB Browser for SQLite to inspect the database.

## FastAPI Endpoints

Here are the key FastAPI endpoints available for managing recipes:

- `GET /recipes`: List all recipes in the database.
- `GET /recipes/{id}`: Retrieve a specific recipe by ID.
- `POST /recipes`: Add a new recipe to the database (manual entry via FastAPI endpoint).

## Troubleshooting

### SQLite OperationalError (No such table)

If you encounter the `sqlite3.OperationalError: no such table` error, it means that the necessary tables have not been created in the database. Ensure the database is properly set up and the models are created. You might need to run database migrations to create the tables (or simply create them manually if needed).

### Import Errors

If the YAML import fails, double-check the format of your YAML files and ensure the `importer/importer.py` script can read the files correctly.

## Conclusion

This FastAPI project allows for easy management and importing of recipe data into an SQLite database. Use the provided scripts and instructions to manage your recipe data effectively and efficiently.

Happy Cooking! 🍕
```


http://localhost:8083/