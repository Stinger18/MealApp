from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
try:
    from app.database import Base
except ImportError:
    from database import Base

''' These classes define the structure of the tables in the database.
    Each class represents a table, and each instance of the class represents a row in the table.
    The __tablename__ attribute specifies the name of the table in the database.
    Each class should inherit from the Base class, which is the declarative base class from SQLAlchemy.
    Each class should define attributes that are instances of Column, which represent columns in the table.
    The Column constructor takes the data type of the column as the first argument, and any additional options as keyword arguments.
    The __repr__ method should return a string representation of the object, which is useful for debugging.
    The __str__ method should return a human-readable string representation of the object, which is useful for displaying the object in the API response.
    The __str__ method is also need for the agent to understand the object and the relationship between information from the object.
'''
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    recipeId = Column(Integer) # ownerID on each recipe
    pantryId = Column(Integer) # ownerID on each pantry item
    shoppingListId = Column(Integer) # ownerID on each shopping list

    def __repr__(self):
        return f'<User: {self.id}, {self.name}, {self.email}, {self.password}, {self.recipeId}, {self.pantryId}, {self.shoppingListId}>'
    
    def __str__(self):
        return f'<User: ID: {self.id}, Name: {self.name}, Recipe Id: {self.recipeId}, Pantry Id: {self.pantryId}, Shopping List Id: {self.shoppingListId}>'


class Recipe(Base):
    ''' This class is the recipe and is the top of the stack. '''
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    ownerId = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    servings = Column(Integer)
    prepTime = Column(String)
    cookTime = Column(String)
    instructions = Column(Text)

    # Relationship with RecipeIngredient table
    recipe_ingredients = relationship('RecipeIngredient', back_populates='recipe')

    def __repr__(self): # Output for debugging
        return f'<Recipe: Id: {self.id}, ownerId: {self.ownerId}, name: {self.name}, description: {self.description}, instructions: {self.instructions}>'


class RecipeIngredient(Base):
    ''' This class connects the recipe and the ingredients while provided new information that IS recipe specific like the quantity. '''
    __tablename__ = 'recipe_ingredients'
    recipeId = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    ingredientId = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantity = Column(String)  # e.g., '2 cups'
    # unit = Column(String)  # e.g., 'cups' #TODO: May add this later
    
    # Relationships to Recipe and Ingredient tables
    recipe = relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = relationship('Ingredient', back_populates='recipe_ingredients')

    def __repr__(self): # Output for debugging
        return f'<RecipeIngredient: recipeId: {self.recipeId}, ingredientId: {self.ingredientId}, quantity: {self.quantity}>'

class Ingredient(Base):
    ''' This class is the ingredients and it's seperated from the recipes. '''
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with RecipeIngredient table
    recipe_ingredients = relationship('RecipeIngredient', back_populates='ingredient')

    def __repr__(self): # Output for debugging
        return f'<Ingredient: Id: {self.id}, name: {self.name}>'

class Pantry(Base):
    __tablename__ = 'pantry'

    id = Column(Integer, primary_key=True, index=True) 
    ownerId = Column(Integer, index=True)
    item = Column(String)
    quantity = Column(Integer)
    date_added = Column(String)

    def __repr__(self):
        return f'<Pantry: ID: {self.id}, Owner ID: {self.ownerId}, Item: {self.item}, Quantity: {self.quantity}, Date Added: {self.date_added}>'
    
    def __str__(self):
        return f'<Pantry: ID: {self.id}, Owner ID: {self.ownerId}, Item: {self.item}, Quantity: {self.quantity}, Date Added: {self.date_added}>'

class Shopping_list(Base):
    __tablename__ = 'shopping list'

    shoppingListId = Column(Integer, primary_key=True, index=True)
    ownerId = Column(Integer, index=True)
    item = Column(String)
    quantity = Column(Integer)
