from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from database import Base, SessionLocal, engine
import pprint


class Recipe(Base):
    __tablename__ = 'recipes2'
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
    __tablename__ = 'recipe_ingredients'
    recipeId = Column(Integer, ForeignKey('recipes2.id'), primary_key=True)
    ingredientId = Column(Integer, ForeignKey('ingredients2.id'), primary_key=True)
    quantity = Column(String)  # e.g., '2 cups'
    # unit = Column(String)  # e.g., 'cups' #TODO: May add this later
    
    # Relationships to Recipe and Ingredient tables
    recipe = relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = relationship('Ingredient', back_populates='recipe_ingredients')

    def __repr__(self): # Output for debugging
        return f'<RecipeIngredient: recipeId: {self.recipeId}, ingredientId: {self.ingredientId}, quantity: {self.quantity}>'

class Ingredient(Base):
    __tablename__ = 'ingredients2'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with RecipeIngredient table
    recipe_ingredients = relationship('RecipeIngredient', back_populates='ingredient')

    def __repr__(self): # Output for debugging
        return f'<Ingredient: Id: {self.id}, name: {self.name}>'


def print_recipe(recipe, index: int = 0, advanced: bool = False) -> dict:
    ''' Formats the recipe for clean output that is ready to become JSON.

    `advanced`: If True, include the recipeId and ownerId. '''
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

''' Create recipe '''
session = SessionLocal()

# This is commented out because the recipe already exists in the database

# Create a new recipe
# newRecipe = Recipe(id=10, ownerId=1, name='Creamy Tuscan Chicken', instructions='1. Cook the chicken. 2. Add the cream. 3. Add the spinach.', servings=4, prepTime='10 minutes', cookTime='20 minutes')
# # Disctionary of ingredients and their quantities
# ingredients = {'Chicken': '2 lbs', 'Cream': '2 cup', 'Spinach': '1 cup'}
# for ingredient, quantity in ingredients.items(): # For each ingredient in the dictionary
#     # Check if the ingredient already exists in the database
#     exsisting_ingredient = session.query(Ingredient).filter(Ingredient.name == ingredient).first()

#     # If the ingredient does not exist, create a new ingredient
#     if not exsisting_ingredient:
#         ingredient = Ingredient(name=ingredient)
#     else: # If the ingredient exists, use the exsisting ingredient
#         ingredient = exsisting_ingredient
    
#     # Associate ingredients with the recipe through the RecipeIngredient table
#     recipe_ingredient = RecipeIngredient(recipe=newRecipe, ingredient=ingredient, quantity=quantity)


# # Add to the session and commit
# session.add(newRecipe)
# session.commit()

# This is if you wanted to see the before changes

# recipe = session.query(Recipe).options(joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient)).all()

# This is how you would update the quantity of an ingredient in a recipe

# recipe_ingredient = session.query(RecipeIngredient).filter_by(recipeId=1, ingredientId=2).first()
# recipe_ingredient.quantity = '1 cup(s)'
# session.commit()


recipe = session.query(Recipe).options(joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient)).all()
pprint.pprint(print_recipe(recipe, advanced=False))

print(session.query(Recipe).all())
print(session.query(RecipeIngredient).all())
print(session.query(Ingredient).all())

# session.query(Recipe).filter(Recipe.id == 10).delete()
# session.query(RecipeIngredient).filter(RecipeIngredient.recipeId == 10).delete()
# session.commit()

# Base.metadata.create_all(bind=engine)
session.close()