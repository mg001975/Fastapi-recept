from pydantic import BaseModel
from typing import List, Optional


# --------------------------------------------------------------
# User login
# --------------------------------------------------------------
class User(BaseModel):
    id: int
    username: str
    hashed_password: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# --------------------------------------------------------------
#
# --------------------------------------------------------------
class StepResponse(BaseModel):
    id: int
    order: int
    description: str

    class Config:
        orm_mode = True


class IngredientResponse(BaseModel):
    id: int
    name: str
    amount: str
    unit: Optional[str] = None

    class Config:
        orm_mode = True


class ComponentResponse(BaseModel):
    id: int
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    steps: List[StepResponse] = []
    ingredients: List[IngredientResponse] = []

    class Config:
        orm_mode = True


class RecipeDetail(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    prep_time: Optional[int] = None
    difficulty: Optional[str] = None
    components: List[ComponentResponse] = []

    class Config:
        orm_mode = True
