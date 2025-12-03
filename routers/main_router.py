from fastapi import APIRouter
from .home_router import router as home_router
from .recipe_router import router as recipe_router
from .crud_router import router as crud_router
from .markdown_router import router as markdown_router
from .admin_router import router as admin_router
from routers.auth_router import auth_router

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_utils import verify_token  # Import your JWT token verification utility
from typing import Dict

main_router = APIRouter()

main_router.include_router(home_router, prefix="", tags=["home"])
main_router.include_router(recipe_router, prefix="/recipe", tags=["recipe"])
main_router.include_router(crud_router, prefix="/crud", tags=["crud"])
main_router.include_router(admin_router, prefix="/admin", tags=["admin"])
main_router.include_router(markdown_router, prefix="/aboutme", tags=["aboutme"])
# Include the login_router
main_router.include_router(auth_router, prefix="/auth", tags=["auth"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Dependency to get the current user by verifying the token
def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    user_data = verify_token(token)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_data


# Add a protected route to the main router
@main_router.get("/protected-route")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}
