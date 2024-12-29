from fastapi import APIRouter
from .home_router import router as home_router
from .recipe_router import router as recipe_router
from .crud_router import router as crud_router
from .markdown_router import router as markdown_router
from .admin_router import router as admin_router

main_router = APIRouter()

main_router.include_router(home_router, prefix="", tags=["home"])
main_router.include_router(recipe_router, prefix="/recipe", tags=["recipe"])
main_router.include_router(crud_router, prefix="/crud", tags=["crud"])
main_router.include_router(admin_router, prefix="/admin", tags=["admin"])
main_router.include_router(markdown_router, prefix="/aboutme", tags=["aboutme"])
