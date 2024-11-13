from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, get_db
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class RecipeCreate(BaseModel):
    title: str
    ingredients: str
    instructions: str

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

''' User Commands '''
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all() # Return all users

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, name=user.name, email=user.email, password=user.password)

''' Recipe Commands '''
def get_recipe(userRecipeId: int, recipeId: int, db:Session = Depends(get_db)):
    return crud.get_recipe(db, userRecipeId=userRecipeId, recipeId=recipeId)

def get_all_recipes(userRecipeId: int, db:Session = Depends(get_db)):
    return crud.get_all_recipes(db, userRecipeId=userRecipeId)

def create_recipe(recipe: RecipeCreate, ownerId: int, db: Session = Depends(get_db)):
    return crud.create_recipe(db=db, ownerId=ownerId, title=recipe.title, ingredients=recipe.ingredients, instructions=recipe.instructions)