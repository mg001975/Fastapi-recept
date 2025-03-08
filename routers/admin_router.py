from fastapi import APIRouter, File, UploadFile, Form, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db

# from database.models import Recipe, RecipeComponent, Step, Ingredient
import yaml

# from io import StringIO
from fastapi.templating import Jinja2Templates

# from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from utils.import_function import insert_recipes_into_db
from utils.export_function import recipes_to_yaml

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")
temp_data = {}


# --------------------------------------------------------------
# Get view
# --------------------------------------------------------------
@router.get("/", response_class=HTMLResponse)
async def import_view(request: Request):
    """
    Render a blank import view.
    """
    return templates.TemplateResponse("admin/import.html", {"request": request})


# --------------------------------------------------------------
# Import
# --------------------------------------------------------------
@router.post("/import_preview", response_class=HTMLResponse)
async def import_preview(request: Request, file: UploadFile = File(...)):
    """
    Handle YAML file upload and display its content as preview.
    """
    print("data loading for preview")

    try:
        # Read the uploaded file
        content = await file.read()
        yaml_data = yaml.safe_load(content)
        preview_data = yaml.dump(yaml_data, sort_keys=False, default_flow_style=False)

    except Exception as e:
        preview_data = f"Error parsing YAML file: {e}"

    return templates.TemplateResponse(
        "admin/import.html",
        {"request": request, "response": preview_data, "yaml_data": yaml_data},
    )


@router.post("/import_data")
async def import_data(yaml_data: str = Form(...), db: Session = Depends(get_db)):
    try:
        data = yaml.safe_load(yaml_data)
        recipes = data.get("Recipes", [])
        print(recipes)

        if not recipes:
            raise ValueError("No 'recipes' found in the provided YAML data.")
        insert_recipes_into_db(recipes, db)

        return RedirectResponse(url="/", status_code=303)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to import data: {e}")


# --------------------------------------------------------------
# Export
# --------------------------------------------------------------
@router.get("/export_recipes")
async def export_recipes(db: Session = Depends(get_db)):
    # Query all recipes from the database
    yaml_data = recipes_to_yaml(db)

    # Define the file path in the root directory
    file_path = os.path.join(os.getcwd(), "recipes.yaml")

    # Write the YAML data to the file
    with open(file_path, "w") as file:
        file.write(yaml_data)

    # Return a success message
    return {"message": f"Recipes exported to {file_path}"}
