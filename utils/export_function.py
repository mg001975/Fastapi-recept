import yaml
from database.models import Recipe, RecipeComponent, Step, Ingredient


def recipes_to_yaml(db):
    """
    Function for exporting recipes to a yaml file for backup.
    """
    # Prepare the data to be exported as YAML
    recipes = db.query(Recipe).all()
    recipes_data = []

    for recipe in recipes:
        recipe_dict = {
            "name": recipe.name,
            "category": recipe.category,
            "description": recipe.description,
            "prep_time": recipe.prep_time,
            "difficulty": recipe.difficulty,
            "RecipeComponent": [],
        }

        # Get the components for this recipe
        components = (
            db.query(RecipeComponent)
            .filter(RecipeComponent.recipe_id == recipe.id)
            .all()
        )

        for component in components:
            component_dict = {
                "component_name": component.name,
                "component_description": component.description,
                "Ingredients": [],
                "Steps": [],
            }

            # Get the ingredients for each component
            ingredients = (
                db.query(Ingredient)
                .filter(Ingredient.component_id == component.id)
                .all()
            )
            for ingredient in ingredients:
                ingredient_dict = {
                    "ingredient_name": ingredient.name,
                    "ingredient_amount": ingredient.amount,
                    "ingredient_unit": ingredient.unit,
                }
                component_dict["Ingredients"].append(ingredient_dict)

            # Get the steps for each component
            steps = db.query(Step).filter(Step.component_id == component.id).all()
            for step in steps:
                step_dict = {
                    "step_order": step.order,
                    "step_description": step.description,
                }
                component_dict["Steps"].append(step_dict)

            recipe_dict["RecipeComponent"].append(component_dict)

        recipes_data.append(recipe_dict)

    return yaml.dump({"Recipes": recipes_data}, sort_keys=False, allow_unicode=True)
