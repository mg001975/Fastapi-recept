import yaml
from typing import List, Dict

from sqlalchemy.orm import Session
from database.models import Recipe, RecipeComponent, Step, Ingredient
from database.database import get_db


def insert_recipes_into_db(recipes_data: List[Dict], db_session: Session):
    """
    Inserts parsed recipes data into the database.

    Args:
        recipes_data (List[Dict]): List of dictionaries containing recipe data.
        db_session (Session): SQLAlchemy session to interact with the database.
    """
    print("Start inserting recipes into the database...")

    for recipe_data in recipes_data:
        print("Recipe data to insert:", recipe_data)
        try:
            # Create Recipe instance
            recipe = Recipe(
                name=recipe_data.get("name", "Unknown Recipe"),
                category=recipe_data.get("category", "Uncategorized"),
                description=recipe_data.get("description", ""),
                prep_time=recipe_data.get("prep_time", None),
                difficulty=recipe_data.get("difficulty", "Unknown"),
            )
            db_session.add(recipe)
            db_session.flush()  # Flush to generate the recipe ID

            print("Recipe added")

            # Handle RecipeComponent
            components_data = recipe_data.get("RecipeComponent", [])
            if isinstance(components_data, dict):
                components_data = [
                    components_data
                ]  # If single component, wrap it in a list

            for component_data in components_data:
                # Create RecipeComponent instance
                component = RecipeComponent(
                    recipe_id=recipe.id,
                    name=component_data.get("component_name", "Unnamed Component"),
                    description=component_data.get("component_description", ""),
                )
                db_session.add(component)
                db_session.flush()  # Flush to generate the component ID
                print("Component created")

                # Handle Ingredients
                ingredients_data = component_data.get("Ingredients", [])
                if isinstance(ingredients_data, dict):
                    ingredients_data = [
                        ingredients_data
                    ]  # Wrap single ingredient in a list

                for ingredient_data in ingredients_data:
                    ingredient = Ingredient(
                        component_id=component.id,
                        name=ingredient_data.get(
                            "ingredient_name", "Unnamed Ingredient"
                        ),
                        amount=ingredient_data.get("ingredient_amount", ""),
                        unit=ingredient_data.get("ingredient_unit", ""),
                    )
                    db_session.add(ingredient)
                    print("Ingredient created")

                # Handle Steps
                steps_data = component_data.get("Steps", [])
                if isinstance(steps_data, dict):
                    steps_data = [steps_data]  # Wrap single step in a list

                for step_data in steps_data:
                    step = Step(
                        order=step_data.get("step_order", "No order"),
                        component_id=component.id,
                        description=step_data.get("step_description", "No Description"),
                    )
                    db_session.add(step)
                    print("Step created")

            db_session.commit()  # Commit all changes
            print(f"Successfully inserted recipe: {recipe.name}")

        except Exception as e:
            print(f"Error inserting recipe '{recipe_data.get('name', 'Unknown')}': {e}")
            db_session.rollback()  # Rollback in case of error


# def insert_recipe_into_db(recipe_data: List[Dict], db_session: Session):
#     """
#     Inserts parsed recipes data into the database.
#     """
#     print("Start inserting recipes into the database...")

#     # for recipe_data in recipes_data:
#     #     # Ensure recipe_data is a dictionary
#     #     if not isinstance(recipe_data, dict):
#     #         print(f"Error: Expected dictionary but got {type(recipe_data)}")
#     #         continue

#     print(f"Inserting recipe: {recipe_data.get('name', 'Unknown Recipe')}")

#     try:
#         # Create Recipe instance
#         recipe = Recipe(
#             name=recipe_data.get("name", "Unknown Recipe"),
#             category=recipe_data.get("category", "Uncategorized"),
#             description=recipe_data.get("description", ""),
#             prep_time=recipe_data.get("prep_time", None),
#             difficulty=recipe_data.get("difficulty", "Unknown"),
#         )

#         db_session.add(recipe)
#         db_session.flush()  # Flush to generate the recipe ID

#         # Handle RecipeComponent
#         components_data = recipe_data.get("RecipeComponent", [])
#         if isinstance(components_data, dict):
#             components_data = [components_data]  # Wrap in a list if single component

#         for component_data in components_data:
#             component = RecipeComponent(
#                 recipe_id=recipe.id,
#                 name=component_data.get("component_name", "Unnamed Component"),
#                 description=component_data.get("component_description", ""),
#             )
#             db_session.add(component)
#             db_session.flush()  # Flush to generate the component ID

#             # Handle Steps
#             steps_data = component_data.get("Steps", [])
#             if isinstance(steps_data, dict):
#                 steps_data = [steps_data]  # Wrap in a list if single step

#             for step_data in steps_data:
#                 step = Step(
#                     component_id=component.id,
#                     description=step_data.get("step_description", "No Description"),
#                 )
#                 db_session.add(step)
#                 db_session.flush()  # Flush to generate the step ID

#                 # Handle Ingredients
#                 ingredients_data = step_data.get("Ingredients", [])
#                 if isinstance(ingredients_data, dict):
#                     ingredients_data = [
#                         ingredients_data
#                     ]  # Wrap in a list if single ingredient

#                 for ingredient_data in ingredients_data:
#                     ingredient = Ingredient(
#                         step_id=step.id,
#                         name=ingredient_data.get(
#                             "ingredient_name", "Unnamed Ingredient"
#                         ),
#                         amount=ingredient_data.get("ingredient_amount", ""),
#                         unit=ingredient_data.get("ingredient_unit", ""),
#                     )
#                     db_session.add(ingredient)

#         db_session.commit()
#         print(f"Successfully inserted recipe: {recipe.name}")

#     except Exception as e:
#         print(f"Error inserting recipe '{recipe_data.get('name', 'Unknown')}': {e}")
#         db_session.rollback()  # Rollback in case of error
