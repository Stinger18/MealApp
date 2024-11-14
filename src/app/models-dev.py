from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from database import Base, SessionLocal

# registry.configure()

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, index=True)
    ownerId = Column(Integer, index=True)
    name = Column(String, nullable=False)
    instructions = Column(Text)

    # Relationship with RecipeIngredient table
    recipe_ingredients = relationship('RecipeIngredient', back_populates='recipe')


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'
    recipeId = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    ingredientId = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantity = Column(String)  # e.g., '2 cups'
    
    # Relationships to Recipe and Ingredient tables
    recipe = relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = relationship('Ingredient', back_populates='recipe_ingredients')

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with RecipeIngredient table
    recipe_ingredients = relationship('RecipeIngredient', back_populates='ingredient')

''' Create recipe '''
session = SessionLocal()
recipeName = Recipe(name='Creamy Tuscan Chicken')
ingredient1 = Ingredient(name="Chicken")
ingredient2 = Ingredient(name="Cream")
ingredient3 = Ingredient(name="Parmesan Cheese")

# Associate ingredients with the recipe through the RecipeIngredient table
recipe_ingredient1 = RecipeIngredient(recipe=recipeName, ingredient=ingredient1, quantity="1 lbs")
recipe_ingredient2 = RecipeIngredient(recipe=recipeName, ingredient=ingredient2, quantity="1 cup")
recipe_ingredient3 = RecipeIngredient(recipe=recipeName, ingredient=ingredient3, quantity="1/2 cup")

# Add to the session and commit
session.add(recipeName)
session.commit()
recipe = session.query(Recipe).options(joinedload(Recipe.ingredients)).all()


print(f'Recipe name: {recipe[0].name}')
for ingredient in recipe[0].ingredients:
    print(f'Ingredient: {ingredient.name}, Quantity: {ingredient.recipe_ingredients[0].quantity}')

session.close()