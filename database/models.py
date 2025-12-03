from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import UUID
from database.database import Base  # Import Base from database.database
from pydantic import BaseModel

# from pydantic import BaseModel, Field

# Base = declarative_base()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None

    def get_uuid(self) -> UUID | None:
        if self.user_id:
            return UUID(self.user_id)
        return None


# --------------------------------------------------------------
# User model
# --------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    description = Column(Text)
    prep_time = Column(Integer)
    difficulty = Column(String)

    components = relationship("RecipeComponent", back_populates="recipe")


class RecipeComponent(Base):
    __tablename__ = "recipe_components"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    name = Column(String, nullable=False)
    description = Column(Text)

    recipe = relationship("Recipe", back_populates="components")

    steps = relationship("Step", back_populates="component")
    ingredients = relationship("Ingredient", back_populates="component")


class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True)

    order = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    component_id = Column(Integer, ForeignKey("recipe_components.id"))

    component = relationship("RecipeComponent", back_populates="steps")


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey("recipe_components.id"))

    name = Column(String, nullable=False)
    amount = Column(String)
    unit = Column(String)

    component = relationship("RecipeComponent", back_populates="ingredients")
