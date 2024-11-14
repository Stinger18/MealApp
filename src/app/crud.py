'''
CRUD Operations \n
This file contains the functions that interact with the database.
'''

from sqlalchemy.orm import Session
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
def get_recipe(db: Session, userRecipeId: int, recipeId: int) -> (models.Recipe | None):
    return db.query(models.Recipe).filter(models.Recipe.id == recipeId, models.Recipe.ownerId == userRecipeId).first()

def get_all_recipes(db: Session, userRecipeId: int) -> list[models.Recipe]:
    return db.query(models.Recipe).filter(models.Recipe.ownerId == userRecipeId).all()

def create_recipe(db: Session, id:int, ownerId: int, title: str, ingredients: str, instructions: str) -> (models.Recipe | None):
    dbRecipe = models.Recipe(id=id, ownerId=ownerId, title=title, ingredients=ingredients, instructions=instructions)
    db.add(dbRecipe)
    db.commit()
    db.refresh(dbRecipe)
    return dbRecipe

def delete_recipe(db: Session, userRecipeId: int, recipeId: int):
    ''' Deletes a recipe with the given recipe ID '''
    db.query(models.Recipe).filter(models.Recipe.id == recipeId, models.Recipe.ownerId == userRecipeId).delete()
    db.commit()
    return

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