from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from auth.jwt_utils import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# @router.get("/", response_class=HTMLResponse)
# def home(request: Request, current_user: dict = Depends(get_current_user)):
#     return templates.TemplateResponse(
#         "home.html", {"request": request, "user": current_user}
#     )
