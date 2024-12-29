from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Recipe

from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")


# --------------------------------------------------------------
# Recipe list
# --------------------------------------------------------------
@router.get("/list")
async def list_recipes(request: Request, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()

    return templates.TemplateResponse(
        "recipe_list.html", {"request": request, "recipes": recipes}
    )


# --------------------------------------------------------------
# Recipe view with id
# --------------------------------------------------------------
@router.get("/{recipe_id:int}", response_class=HTMLResponse)
async def view_recipe(recipe_id: int, request: Request, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        return {"error": "Recipe not found"}

    return templates.TemplateResponse(
        "view_recipe.html", {"request": request, "recipe": recipe}
    )
