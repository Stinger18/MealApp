"""
main.py

This file is mainly used to run the FastAPI server.
To run the server:
1) Navigate to the website directory and use the command `python -m http.server 8000`
to start the test frontend. Otherwise, follow the steps for the frontend.
2) In a new terminal, use the command `uvicorn app.main:app --reload` form Whats-for-Dinner\\src. This will stay running.
You can stop it with ctrl+c.
3) Navigate to `http://localhost:8000` or whatever the url will be in a web browser to see the frontend.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
try:
    from app.errorHandling import EmailAlreadyExists
    from app import models, crud
    from app.database import SessionLocal, get_db, engine
except ImportError:
    from errorHandling import EmailAlreadyExists
    import models, crud
    from database import SessionLocal, get_db, engine

import random

# Create the database tables
# models.Base.metadata.create_all(bind=engine)

from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class RecipeCreate(BaseModel):
    title: str
    ingredients: dict
    instructions: str
    servings: int
    prepTime: str
    cookTime: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"], # Allow requests from the frontend TODO: Update this to the frontend URL
    # allow_credentials=True,
    allow_methods=["POST", "GET"], # Allow POST and GET requests
    allow_headers=["*"], # Allow all headers
)

''' User Commands '''
@app.get("/users/{userId}")
def get_user(userId: int, db: Session = Depends(get_db)):
    return crud.get_user(db, userId=userId)

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all() # Return all users

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    ''' Creates a new user if the email does not already exist '''
    # Check if the email already exists
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise EmailAlreadyExists(email=user.email)
    # Proceed if email does not exist
    userDBID = random.randint(1, 100)
    return crud.create_user(db=db, id=len(db.query(models.User).all())+1, name=user.name, email=user.email, password=user.password, recipeId=userDBID, pantryId=userDBID, shoppingListId=userDBID) #TODO: Update for the new structure

''' Recipe Commands '''
def get_recipe(userRecipeId: int, recipeId: int, advancedFormat: bool = False, db:Session = Depends(get_db)):
    return crud.get_recipe(db, userRecipeId=userRecipeId, recipeId=recipeId, advancedFormat=advancedFormat)

def get_all_recipes(userRecipeId: int, db:Session = Depends(get_db)):
    return crud.get_all_recipes(db, userRecipeId=userRecipeId)

def create_recipe(recipe: RecipeCreate, ownerId: int, db: Session = Depends(get_db)):
    return crud.create_recipe(db=db, id=len(db.query(models.Recipe).all())+1, ownerId=ownerId, title=recipe.title, ingredients=recipe.ingredients, instructions=recipe.instructions, servings=recipe.servings, prepTime=recipe.prepTime, cookTime=recipe.cookTime)


if __name__ == "__main__":
    ''' Use this to create a test data from here '''
    # crud.create_user(db=SessionLocal(), id=1, name="Test User", email="email@gmail.com", password="password", recipeId=1, pantryId=1, shoppingListId=1)
    # testUser = get_user(1, db=SessionLocal())
    # print(testUser.name)

    # crud.create_recipe(db=SessionLocal(), id=2, ownerId=1, name='Creamy Tuscan Chicken', ingredients={'Chicken': '2 lbs', 'Cream': '2 cup', 'Spinach': '1 cup'}, instructions="1. Season the chicken with salt and pepper. 2. Heat the oil in a large skillet over medium-high heat. 3. Add the chicken and cook until golden brown on both sides. 4. Remove the chicken from the skillet and set aside. 5. Add the garlic to the skillet and cook until fragrant. 6. Add the spinach and sun-dried tomatoes and cook until the spinach is wilted. 7. Add the heavy cream and parmesan cheese and bring to a simmer. 8. Return the chicken to the skillet and cook until the sauce has thickened. 9. Serve the chicken with the sauce.", servings=4, prepTime='10 minutes', cookTime='20 minutes')
    # testRecipe = get_recipe(1, 1, db=SessionLocal())
    # print(testRecipe.title)

    SessionLocal().close()
