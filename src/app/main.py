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
from langgraph.graph.state import CompiledStateGraph # Used for typing
from langchain_core.messages import HumanMessage # Used for typing
try:
    print("Importing from app")
    from app.errorHandling import EmailAlreadyExists
    from app import models, crud
    from app.database import SessionLocal, get_db, engine
    from app.agent import buildSousChef
    from app.image_detect import get_ingredients
    print("Imported from app")
except ImportError:
    print("Importing from main")
    from errorHandling import EmailAlreadyExists
    import models, crud
    from database import SessionLocal, get_db, engine
    from agent import buildSousChef
    from image_detect import get_ingredients

import random
from datetime import date

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
    allow_origins=["http://localhost:3000"], # Allow requests from the frontend TODO: Update this to the frontend URL
    # allow_credentials=True,
    allow_methods=["POST", "GET"], # Allow POST and GET requests
    allow_headers=["*"], # Allow all headers
)

''' Create the agent instance '''
# For testing purposes
#TODO: Update this to use the active users information
user: (models.User | None) = crud.get_user_by_id(db=SessionLocal(), userId=1)
sousChef: CompiledStateGraph = buildSousChef(userInfo=user) # Create the agent with the test users data

''' User Commands '''
@app.get("/users/{userId}")
def get_user(userId: int, db: Session = Depends(get_db)): # TODO: Update to get user by name or id
    return crud.get_user_by_id(db, userId=userId)

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

''' Agent Commands '''

@app.get("/agent/{query}")
def query_agent(query: str, simple: bool = False):
    ''' Query the agent with the given query '''
    if simple: # Return only the last response
        return sousChef.invoke({"messages": [HumanMessage(content=query)]},
                config={"configurable": {"thread_id": 42}})["messages"]["content"]
    else: # Return all responses
        return sousChef.invoke({"messages": [HumanMessage(content=query)]},
                config={"configurable": {"thread_id": 42}})

''' Recipe Commands '''
@app.get("/recipes/{userRecipeId}/{recipeId}")
def get_recipe(userRecipeId: int, recipeId: int, advancedFormat: bool = False, db:Session = Depends(get_db)):
    return crud.get_recipe(db, userRecipeId=userRecipeId, recipeId=recipeId, advancedFormat=advancedFormat)

@app.get("/recipes/{userRecipeId}")
def get_all_recipes(userRecipeId: int, db:Session = Depends(get_db)):
    return crud.get_all_recipes(db, userRecipeId=userRecipeId)

@app.post("/recipes/{ownerId}")
def create_recipe(recipe: RecipeCreate, ownerId: int, db: Session = Depends(get_db)):
    return crud.create_recipe(db=db, id=len(db.query(models.Recipe).all())+1, ownerId=ownerId, title=recipe.title, ingredients=recipe.ingredients, instructions=recipe.instructions, servings=recipe.servings, prepTime=recipe.prepTime, cookTime=recipe.cookTime)

''' Pantry Commands '''
@app.get("/pantry/{pantryId}")
def get_pantry(pantryId: int, db: Session = Depends(get_db)):
    return crud.get_pantry(db, userPantryId=pantryId)

@app.post("/pantry/{pantryId}/add")
def add_to_pantry(pantryId: int, ingredients: dict, db: Session = Depends(get_db)):
    for key, value in ingredients.items():
        crud.add_to_pantry(db, id=len(crud.get_pantry(db, userPantryId=pantryId))+1, ownerId=pantryId, item=key, quantity=value, date_added=date.today())
    return {"message": "Ingredients added to pantry"}

@app.post("/pantry/{pantryId}/remove")
def remove_from_pantry(pantryId: int, itemId: int, db: Session = Depends(get_db)):
    crud.remove_from_pantry(db, ownerId=pantryId, itemId=itemId)
    return {"message": "Ingredient removed from pantry"}

'''Image Detection Commands'''
@app.get("/image/{url}")
def detect_image(url: str):
    return get_ingredients(url)


if __name__ == "__main__":
    ''' Use this to create a test data from here '''
    # crud.create_user(db=SessionLocal(), id=1, name="Test User", email="email@gmail.com", password="password", recipeId=1, pantryId=1, shoppingListId=1)
    # testUser = crud.get_user_by_id(db=SessionLocal(), userId=1) 
    # print(testUser)
    # itemsToAdd = {'Cream of Chicken Soup': '2', 'Chicken': '2 lbs', 'Cream': '2 cup', 'Spinach': '1 cup'}
    # add_to_pantry(db=SessionLocal(), pantryId=1, ingredients=itemsToAdd)
    testPantry = crud.get_pantry(db=SessionLocal(), userPantryId=1)
    print(f'Pantry: {testPantry}')

    # crud.create_recipe(db=SessionLocal(), id=2, ownerId=1, name='Creamy Tuscan Chicken', ingredients={'Chicken': '2 lbs', 'Cream': '2 cup', 'Spinach': '1 cup'}, instructions="1. Season the chicken with salt and pepper. 2. Heat the oil in a large skillet over medium-high heat. 3. Add the chicken and cook until golden brown on both sides. 4. Remove the chicken from the skillet and set aside. 5. Add the garlic to the skillet and cook until fragrant. 6. Add the spinach and sun-dried tomatoes and cook until the spinach is wilted. 7. Add the heavy cream and parmesan cheese and bring to a simmer. 8. Return the chicken to the skillet and cook until the sauce has thickened. 9. Serve the chicken with the sauce.", servings=4, prepTime='10 minutes', cookTime='20 minutes')
    # testRecipe = get_recipe(1, 1, db=SessionLocal())
    # print(testRecipe.title)

    SessionLocal().close()
