'''
CRUD Operations \n
This file contains the functions that interact with the database.
'''

from sqlalchemy.orm import Session, joinedload
try:
    from app import models
except ImportError:
    import models
from passlib.context import CryptContext

''' User Operations '''
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_id(db: Session, userId: int) -> (models.User | None):
    ''' Returns the user (User) with the given ID'''
    return db.query(models.User).filter(models.User.id == userId).first()

def get_user_by_name(db: Session, userName: str) -> (models.User | None):
    ''' Returns the user (User) with the given name'''
    return db.query(models.User).filter(models.User.name == userName).first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, id: int, name: str, email:str, password: str, recipeId: int, pantryId: int, shoppingListId: int) -> (models.User | None):
    hashed_password = pwd_context.hash(password)
    dbUser = models.User(id=id, name=name, email=email, password=hashed_password, recipeId=recipeId, pantryId=pantryId, shoppingListId=shoppingListId)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser

''' Recipe Operations '''
def get_recipe(db: Session, userRecipeId: int, recipeId: int, advancedFormat: bool = False) -> (models.Recipe | None):
    recipe = db.query(models.Recipe).options(joinedload(models.Recipe.recipe_ingredients).joinedload(models.RecipeIngredient.ingredient)).filter(models.Recipe.id == recipeId, models.Recipe.ownerId == userRecipeId).first()
    return format_recipe(recipe, advanced=advancedFormat)

def get_all_recipes(db: Session, userRecipeId: int) -> list[models.Recipe]: #TODO: Can add the format_recipe function here but it needs to be updarte to loop over all recipes in the list
    return db.query(models.Recipe).options(joinedload(models.Recipe.recipe_ingredients).joinedload(models.RecipeIngredient.ingredient)).filter(models.Recipe.ownerId == userRecipeId).all()

def create_recipe(db: Session, id: int, ownerId: int, name: str, ingredients: dict, instructions: str, servings: int, prepTime: str, cookTime: str):
    ''' Mock CRUD operation to create a recipe 
    
    `ingredients` is a dictionary with the ingredient name as the key and the quantity as the value. \n
    `{'Chicken': '2 lbs', 'Cream': '2 cup', 'Spinach': '1 cup'}` '''
    # Create a new recipe
    dbRecipe = models.Recipe(id=id, ownerId=ownerId, name=name, instructions=instructions, servings=servings, prepTime=prepTime, cookTime=cookTime)

    # Disctionary of ingredients and their quantities
    ingredients = ingredients

    for ingredient, quantity in ingredients.items(): # For each ingredient in the dictionary
        # Check if the ingredient already exists in the database
        exsisting_ingredient = db.query(models.Ingredient).filter(models.Ingredient.name == ingredient).first()

        # If the ingredient does not exist, create a new ingredient
        if not exsisting_ingredient:
            ingredient = models.Ingredient(name=ingredient)
        else: # If the ingredient exists, use the exsisting ingredient
            ingredient = exsisting_ingredient
        
        # Associate ingredients with the recipe through the RecipeIngredient table
        models.RecipeIngredient(recipe=dbRecipe, ingredient=ingredient, quantity=quantity)
    # Add to the session and commit
    db.add(dbRecipe)
    db.commit()
    db.refresh(dbRecipe)
    return dbRecipe

def delete_recipe(db: Session, userRecipeId: int, recipeId: int):
    ''' Deletes a recipe with the given recipe ID '''
    db.query(models.Recipe).filter(models.Recipe.id == recipeId, models.Recipe.ownerId == userRecipeId).delete()
    db.commit()
    return

def format_recipe(recipe, index: int = 0, advanced: bool = False) -> dict:
    ''' Formats the recipe for clean output that is ready to become JSON. Returns a `dict` object.

    `advanced`: If True, include the recipeId and ownerId. 
    
    Use `pprint.pprint(format_recipe(recipe))` to print the formatted recipe. '''
    # Dictionary to hold the recipe
    recipeDict = {'name': recipe[index].name, 'description': recipe[index].description, 'servings': recipe[index].servings, 'prepTime': recipe[index].prepTime, 'cookTime': recipe[index].cookTime, 'ingredients': [],'instructions': recipe[index].instructions}

    for recipe_ingredient in recipe[index].recipe_ingredients: # Loop over the ingredients
        ingredient = recipe_ingredient.ingredient

        if advanced: # If the advanced flag is set, include the recipeId and ownerId
            recipeDict['ingredients'].append({"name": ingredient.name, "quantity": recipe_ingredient.quantity, 'recipeId': recipe_ingredient.recipeId, 'ingredientId': recipe_ingredient.ingredientId}) #TODO: If we store the unit, add it here
        else:
            recipeDict['ingredients'].append({"name": ingredient.name, "quantity": recipe_ingredient.quantity})

    if advanced: # If the advanced flag is set, include the recipeId and ownerId
        recipeDict['recipeId'] = recipe[index].id
        recipeDict['ownerId'] = recipe[index].ownerId
        return recipeDict
    else:
        return recipeDict

''' Pantry Operations '''
def get_pantry(db: Session, userPantryId: int) -> (models.Pantry | None):
    ''' Returns each item in the users pantry '''
    return db.query(models.Pantry).filter(models.Pantry.ownerId == userPantryId).all()

def add_to_pantry(db: Session, id: int, ownerId: int, item: str, quantity: int, date_added: str) -> (models.Pantry | None):
    ''' Adds a item to the users pantry '''
    dbPantry = models.Pantry(id=id, ownerId=ownerId, item=item, quantity=quantity, date_added=date_added)
    db.add(dbPantry)
    db.commit()
    db.refresh(dbPantry)
    return dbPantry

def remove_from_pantry(db: Session, userPantryId: int, itemId: int):
    ''' Remove an item of the given item ID from the users pantry '''
    db.query(models.Pantry).filter(models.Pantry.id == itemId, models.Pantry.ownerId == userPantryId).delete()
    db.commit()
    return