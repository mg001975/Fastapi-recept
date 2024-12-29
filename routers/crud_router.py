from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Recipe, RecipeComponent, Ingredient, Step

from fastapi import Request, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# --------------------------------------------------------------
# Recipe view
# --------------------------------------------------------------
@router.get("/")
async def list_recipes(request: Request, db: Session = Depends(get_db)):
    # Query all recipes
    recipes = db.query(Recipe).all()

    return templates.TemplateResponse(
        "crud/recipe_list.html", {"request": request, "recipes": recipes}
    )


# --------------------------------------------------------------
# Recipe form
# --------------------------------------------------------------
@router.get("/get_recipe", response_class=HTMLResponse)
@router.get("/get_recipe/{recipe_id}", response_class=HTMLResponse)
async def get_recipe_form(recipe_id: int = None, db: Session = Depends(get_db)):
    recipe = None
    components = []

    if recipe_id:
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            logger.error(f"Recipe with ID {recipe_id} not found.")
            raise HTTPException(status_code=404, detail="Recipe not found")
        logger.debug(f"Fetched recipe: {recipe}")

        components = (
            db.query(RecipeComponent)
            .filter(RecipeComponent.recipe_id == recipe.id)
            .all()
        )
        logger.debug(f"Fetched components: {components}")

        # Fetch steps and ingredients for each component
        for component in components:
            component_steps = (
                db.query(Step).filter(Step.component_id == component.id).all()
            )
            component.steps = component_steps  # Attach steps to the component
            logger.debug(
                f"Fetched steps for component {component.id}: {component_steps}"
            )

            component.ingredients = (
                db.query(Ingredient)
                .filter(Ingredient.component_id == component.id)
                .all()
            )
            logger.debug(
                f"Fetched ingredients for step {component.id}: {component.ingredients}"
            )

    logger.info(f"Final recipe: {recipe}")
    logger.info(f"Final components: {components}")

    return templates.TemplateResponse(
        "crud/main_form.html",
        {
            "request": {},
            "recipe": recipe,
            "components": components,
        },
    )


# --------------------------------------------------------------
# Recipe
# --------------------------------------------------------------
@router.post("/create_recipe", response_model=dict)
async def create_recipe(
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(None),
    prep_time: int = Form(None),
    difficulty: str = Form(None),
    db: Session = Depends(get_db),
):
    new_recipe = Recipe(
        name=name,
        description=description,
        category=category,
        prep_time=prep_time,
        difficulty=difficulty,
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return RedirectResponse(url=f"/crud/get_recipe/{new_recipe.id}", status_code=303)


# edit recipe
@router.post("/edit_recipe/{recipe_id}", response_model=dict)
async def edit_recipe(
    recipe_id: int,
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(None),
    prep_time: int = Form(None),
    difficulty: str = Form(None),
    db: Session = Depends(get_db),
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Update the fields
    recipe.name = name
    recipe.description = description
    recipe.category = category
    recipe.prep_time = prep_time
    recipe.difficulty = difficulty

    db.commit()
    db.refresh(recipe)
    return RedirectResponse(url=f"/crud/get_recipe/{recipe_id}", status_code=303)


# Delete recipe
@router.delete("/delete_recipe/{recipe_id}")
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe {recipe_id} not found")

    db.delete(recipe)
    db.commit()

    return RedirectResponse(url=f"/", status_code=303)


# --------------------------------------------------------------
# Component
# --------------------------------------------------------------
@router.post("/create_component")
async def create_component(
    name: str = Form(...),
    description: str = Form(...),
    recipe_id: int = Form(...),  # Associate the component with a recipe
    db: Session = Depends(get_db),
):
    """
    Create a new recipe component and associate it with a recipe.
    """
    component = RecipeComponent(name=name, description=description, recipe_id=recipe_id)
    db.add(component)
    db.commit()
    db.refresh(component)
    return RedirectResponse(url=f"/crud/get_recipe/{recipe_id}", status_code=303)


@router.post("/edit_component/{component_id}")
async def edit_component(
    component_id: int = Path(...),
    name: str = Form(...),
    description: str = Form(...),
    recipe_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """
    Edit an existing recipe component by ID.
    """
    component = (
        db.query(RecipeComponent).filter(RecipeComponent.id == component_id).first()
    )
    if not component:
        return {"error": "Component not found"}

    component.name = name
    component.description = description
    component.recipe_id = recipe_id
    db.commit()
    db.refresh(component)

    return RedirectResponse(url=f"/crud/get_recipe/{recipe_id}", status_code=303)


@router.post("/delete_component/{component_id}")
async def delete_component(component_id: int, db: Session = Depends(get_db)):
    component = db.query(RecipeComponent()).filter(component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Step not found")
    db.delete(component)
    db.commit()
    return {"detail": "Step deleted successfully"}


# --------------------------------------------------------------
# Step
# --------------------------------------------------------------


@router.post("/create_step")
async def create_step(
    new_order: int = Form(...),
    new_step_description: str = Form(...),
    component_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """
    Create a new step and associate it with a component.
    """
    step = Step(
        description=new_step_description, order=new_order, component_id=component_id
    )
    db.add(step)
    db.commit()
    db.refresh(step)

    recipe_id = step.component.recipe.id

    return RedirectResponse(url=f"/crud/get_recipe/{recipe_id}", status_code=303)


@router.post("/edit_step/{step_id}")
async def edit_step(
    step_id: int = Path(...),
    order: int = Form(...),
    description: str = Form(...),
    component_id: int = Form(...),
    db: Session = Depends(get_db),
):
    step = db.query(Step).filter(Step.id == step_id).first()
    if step:
        step.order = order
        step.description = description
        step.component_id = component_id
        db.commit()
        db.refresh(step)

        return RedirectResponse(
            url=f"/crud/get_recipe/{step.component.recipe_id}", status_code=303
        )
    return {"error": "Step not found"}


@router.delete("/delete_step/{step_id}", response_model=dict)
async def delete_step(step_id: int, db: Session = Depends(get_db)):
    step = db.query(Step).filter(Step.id == step_id).first()

    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    db.delete(step)
    db.commit()

    return {"detail": "Step deleted successfully"}


# --------------------------------------------------------------
# Ingredient
# --------------------------------------------------------------
@router.post("/create_ingredient")
async def create_ingredient(
    new_ingredient_name: str = Form(...),
    new_ingredient_amount: int = Form(...),
    new_ingredient_unit: str = Form(...),
    component_id: int = Form(...),
    db: Session = Depends(get_db),
):
    ingredient = Ingredient(
        name=new_ingredient_name,
        amount=new_ingredient_amount,
        unit=new_ingredient_unit,
        component_id=component_id,
    )
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)

    recipe_id = ingredient.component.recipe.id

    return RedirectResponse(url=f"/crud/get_recipe/{recipe_id}", status_code=303)


@router.post("/edit_ingredient/{ingredient_id}")
async def edit_ingredient(
    ingredient_id: int = Path(...),
    ingredient_name: str = Form(...),
    ingredient_amount: int = Form(...),
    ingredient_unit: str = Form(...),
    component_id: int = Form(...),
    db: Session = Depends(get_db),
):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

    if ingredient:
        ingredient.name = ingredient_name
        ingredient.amount = ingredient_amount
        ingredient.unit = ingredient_unit
        ingredient.component_id = component_id

        db.commit()
        db.refresh(ingredient)

        return RedirectResponse(
            url=f"/crud/get_recipe/{ingredient.component.recipe.id}",
            status_code=303,
        )

    return {"error": "Step not found"}


@router.delete("/delete_ingredient/{ingredient_id}", response_model=dict)
async def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    print(ingredient_id)
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    print(ingredient)

    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    db.delete(ingredient)
    db.commit()

    return {"message": f"Ingredient {ingredient_id} deleted successfully"}
