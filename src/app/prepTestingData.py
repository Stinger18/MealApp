'''
Use this file to create test data in the database
'''
from sqlalchemy.orm import Session
from database import SessionLocal
import models, crud, database, schemas, modelsDev

def create_test_recipe_new_model(db: Session, id: int, ownerId: int, name: str, ingredients: dict, instructions: str, servings: int, prepTime: str, cookTime: str):
    ''' Mock CRUD operation to create a recipe 
    
    `ingredients` is a dictionary with the ingredient name as the key and the quantity as the value. \n
    `{'Chicken': '2 lbs', 'Cream': '2 cup', 'Spinach': '1 cup'}` '''
    # Create a new recipe
    newRecipe = modelsDev.Recipe(id=id, ownerId=ownerId, name=name, instructions=instructions, servings=servings, prepTime=prepTime, cookTime=cookTime)

    # Disctionary of ingredients and their quantities
    ingredients = ingredients

    for ingredient, quantity in ingredients.items(): # For each ingredient in the dictionary
        # Check if the ingredient already exists in the database
        exsisting_ingredient = db.query(modelsDev.Ingredient).filter(modelsDev.Ingredient.name == ingredient).first()

        # If the ingredient does not exist, create a new ingredient
        if not exsisting_ingredient:
            ingredient = modelsDev.Ingredient(name=ingredient)
        else: # If the ingredient exists, use the exsisting ingredient
            ingredient = exsisting_ingredient
        
        # Associate ingredients with the recipe through the RecipeIngredient table
        modelsDev.RecipeIngredient(recipe=newRecipe, ingredient=ingredient, quantity=quantity)
    # Add to the session and commit
    db.add(newRecipe)
    db.commit()

db = SessionLocal()

create_test_recipe_new_model(id=2, ownerId=1, name='Creamy Tuscan Chicken', ingredients={'Chicken': '2 lbs', 'Cream': '2 cup', 'Spinach': '1 cup'}, instructions='1. Cook the chicken. 2. Add the cream. 3. Add the spinach.', servings=4, prepTime='10 minutes', cookTime='20 minutes')