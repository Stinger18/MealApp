from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
import models
from database import SessionLocal, get_db, engine

# # Create the database tables
# models.Base.metadata.create_all(bind=engine)

from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    id: int
    name: str
    email: str
    password: str
    recipeId: int
    pantryId: int
    shoppingListId: int

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
    return crud.create_user(db=db, name=user.name, email=user.email, password=user.password) #TODO: Update for the new structure

''' Recipe Commands '''
def get_recipe(userRecipeId: int, recipeId: int, db:Session = Depends(get_db)):
    return crud.get_recipe(db, userRecipeId=userRecipeId, recipeId=recipeId)

def get_all_recipes(userRecipeId: int, db:Session = Depends(get_db)):
    return crud.get_all_recipes(db, userRecipeId=userRecipeId)

def create_recipe(recipe: RecipeCreate, ownerId: int, db: Session = Depends(get_db)):
    return crud.create_recipe(db=db, ownerId=ownerId, title=recipe.title, ingredients=recipe.ingredients, instructions=recipe.instructions)

# crud.create_user(db=SessionLocal(), id=1, name="Test User", email="email@gmail.com", password="password", recipeId=1, pantryId=1, shoppingListId=1)
print(read_user(1, db=SessionLocal()))
SessionLocal().close()
