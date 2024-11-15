from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from database import Base, SessionLocal, engine



class Recipe(Base):
    __tablename__ = 'recipes2'
    id = Column(Integer, primary_key=True, index=True)
    ownerId = Column(Integer, index=True)
    name = Column(String, nullable=False)
    instructions = Column(Text)

    # Relationship with RecipeIngredient table
    recipe_ingredients = relationship('RecipeIngredient', back_populates='recipe')


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'
    recipeId = Column(Integer, ForeignKey('recipes2.id'), primary_key=True)
    ingredientId = Column(Integer, ForeignKey('ingredients2.id'), primary_key=True)
    quantity = Column(String)  # e.g., '2 cups'
    
    # Relationships to Recipe and Ingredient tables
    recipe = relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = relationship('Ingredient', back_populates='recipe_ingredients')

class Ingredient(Base):
    __tablename__ = 'ingredients2'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with RecipeIngredient table
    recipe_ingredients = relationship('RecipeIngredient', back_populates='ingredient')

''' Create recipe '''
session = SessionLocal()

# This is commented out because the recipe already exists in the database

# # Create a new recipe
# newRecipe = Recipe(name='Creamy Tuscan Chicken')
# # Disctionary of ingredients and their quantities
# ingredients = {'Chicken': '2 lbs', 'Cream': '2 cup'}
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


# print(f'Recipe name: {recipe[0].name}')
# for recipe_ingredient in recipe[0].recipe_ingredients:
#     # print(ingredient.ingredient.name)
#     ingredient = recipe_ingredient.ingredient
#     print(f'Ingredient: {ingredient.name}, Quantity: {recipe_ingredient.quantity}, recipe_id: {recipe_ingredient.recipeId}, ingredient_id: {recipe_ingredient.ingredientId}')

# This is how you would update the quantity of an ingredient in a recipe

# recipe_ingredient = session.query(RecipeIngredient).filter_by(recipeId=1, ingredientId=2).first()
# recipe_ingredient.quantity = '1 cup(s)'
# session.commit()


recipe = session.query(Recipe).options(joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient)).all()


print(f'Recipe name: {recipe[0].name}')
for recipe_ingredient in recipe[0].recipe_ingredients:
    # print(ingredient.ingredient.name)
    ingredient = recipe_ingredient.ingredient
    print(f'Ingredient: {ingredient.name}, Quantity: {recipe_ingredient.quantity}, recipe_id: {recipe_ingredient.recipeId}, ingredient_id: {recipe_ingredient.ingredientId}')

session.close()
# Base.metadata.create_all(bind=engine)