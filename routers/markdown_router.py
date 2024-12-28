import os
import markdown
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
def about(request: Request):
    project_root = Path(__file__).resolve().parents[1]
    readme_path = project_root / "readme.md"
    print(readme_path)

    if not os.path.isfile(readme_path):
        return templates.TemplateResponse(
            "about.html",
            {"request": request, "readme_html": "<p>README.md file not found.</p>"},
        )

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    html_content = markdown.markdown(
        readme_content, extensions=["extra", "codehilite", "toc"]
    )

    return templates.TemplateResponse(
        "about.html",
        {"request": request, "readme_html": html_content},
    )
