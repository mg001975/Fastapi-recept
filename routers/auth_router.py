from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from auth.jwt_utils import create_access_token  # your JWT generation function
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# Create a new APIRouter instance
auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define the login request model
class UserLoginRequest(BaseModel):
    username: str
    password: str


@auth_router.post("/login")
def login(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create JWT
    token = create_access_token(data={"sub": user.username})

    # Set token in cookie
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True if using HTTPS
        samesite="lax",
    )
    return response


@auth_router.post("/logout")
def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("access_token")
    return response
