import React, { useState } from 'react';
import RecipeCard from './RecipeCard';
import RecipeTile from './RecipeTile';
import './RecipeBox.css';

function RecipeBox() {
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  const recipes = [
    {
      "recipeName": "Classic Spaghetti Bolognese",
      "description": "A hearty and flavorful Italian pasta dish with a rich, meaty sauce.",
      "prepTime": "15 minutes",
      "cookTime": "1 hour",
      "totalTime": "1 hour 15 minutes",
      "servings": 4,
      "ingredients": [
        { "name": "Olive oil", "quantity": "2", "unit": "tablespoons" },
        { "name": "Onion", "quantity": "1", "unit": "large, finely chopped" },
        { "name": "Carrot", "quantity": "1", "unit": "large, diced" },
        { "name": "Celery", "quantity": "2", "unit": "stalks, diced" },
        { "name": "Ground beef", "quantity": "1", "unit": "pound" },
        { "name": "Garlic", "quantity": "3", "unit": "cloves, minced" },
        { "name": "Tomato paste", "quantity": "2", "unit": "tablespoons" },
        { "name": "Canned tomatoes", "quantity": "28", "unit": "ounces, crushed" },
        { "name": "Red wine", "quantity": "1/2", "unit": "cup" },
        { "name": "Italian seasoning", "quantity": "1", "unit": "teaspoon" },
        { "name": "Salt", "quantity": "to taste", "unit": null },
        { "name": "Black pepper", "quantity": "to taste", "unit": null },
        { "name": "Spaghetti", "quantity": "1", "unit": "pound, cooked" },
        { "name": "Parmesan cheese", "quantity": "to taste", "unit": "grated" }
      ],
      "steps": [
        "Heat the olive oil in a large skillet over medium heat.",
        "Add the onion, carrot, and celery. Sauté until softened, about 5 minutes.",
        "Add the ground beef and cook until browned, breaking it apart with a spoon, about 8 minutes.",
        "Stir in the garlic and cook for 1 minute until fragrant.",
        "Mix in the tomato paste and cook for 2 minutes to deepen the flavor.",
        "Pour in the red wine, scraping the bottom of the skillet to deglaze, and simmer for 3 minutes.",
        "Add the crushed tomatoes, Italian seasoning, salt, and black pepper. Stir to combine.",
        "Reduce the heat to low, cover, and let the sauce simmer for 45 minutes, stirring occasionally.",
        "Cook the spaghetti according to package instructions. Drain and set aside.",
        "Serve the Bolognese sauce over the spaghetti. Top with grated Parmesan cheese."
      ],
      "nutrition": {
        "calories": 450,
        "protein": "20g",
        "fat": "15g",
        "carbohydrates": "50g",
        "fiber": "4g"
      }
    },
    {
      "recipeName": "Chicken Stir Fry",
      "description": "Quick and healthy Asian-inspired dish with fresh vegetables.",
      "prepTime": "20 minutes",
      "cookTime": "10 minutes",
      "totalTime": "30 minutes",
      "servings": 4,
      "ingredients": [
        { "name": "Chicken breast", "quantity": "1", "unit": "pound, sliced thinly" },
        { "name": "Soy sauce", "quantity": "1/4", "unit": "cup" },
        { "name": "Cornstarch", "quantity": "1", "unit": "tablespoon" },
        { "name": "Vegetable oil", "quantity": "2", "unit": "tablespoons" },
        { "name": "Garlic", "quantity": "3", "unit": "cloves, minced" },
        { "name": "Ginger", "quantity": "1", "unit": "teaspoon, grated" },
        { "name": "Broccoli", "quantity": "2", "unit": "cups, chopped" },
        { "name": "Bell pepper", "quantity": "1", "unit": "sliced" },
        { "name": "Carrot", "quantity": "1", "unit": "sliced" },
        { "name": "Oyster sauce", "quantity": "3", "unit": "tablespoons" },
        { "name": "Chicken stock", "quantity": "1/4", "unit": "cup" },
        { "name": "Salt", "quantity": "to taste", "unit": null }
      ],
      "steps": [
        "In a bowl, mix soy sauce and cornstarch. Add sliced chicken and marinate for 10 minutes.",
        "Heat vegetable oil in a wok or large skillet over high heat.",
        "Add garlic and ginger, sautéing for 30 seconds until fragrant.",
        "Stir-fry the chicken until cooked through, about 5 minutes. Remove and set aside.",
        "Add broccoli, bell pepper, and carrot to the skillet. Cook for 3–4 minutes.",
        "Return the chicken to the skillet and mix in oyster sauce and chicken stock.",
        "Stir-fry everything for 2 minutes until the sauce thickens. Serve immediately."
      ],
      "nutrition": {
        "calories": 300,
        "protein": "25g",
        "fat": "10g",
        "carbohydrates": "20g",
        "fiber": "3g"
      }
    },
    {
      "recipeName": "Vegetarian Pizza",
      "description": "Homemade pizza loaded with fresh vegetables and melted cheese.",
      "prepTime": "25 minutes",
      "cookTime": "15 minutes",
      "totalTime": "40 minutes",
      "servings": 6,
      "ingredients": [
        { "name": "Pizza dough", "quantity": "1", "unit": "store-bought or homemade" },
        { "name": "Pizza sauce", "quantity": "1/2", "unit": "cup" },
        { "name": "Mozzarella cheese", "quantity": "2", "unit": "cups, shredded" },
        { "name": "Mushrooms", "quantity": "1", "unit": "cup, sliced" },
        { "name": "Bell peppers", "quantity": "1", "unit": "cup, sliced" },
        { "name": "Red onion", "quantity": "1/2", "unit": "cup, sliced" },
        { "name": "Olives", "quantity": "1/4", "unit": "cup, sliced" },
        { "name": "Italian seasoning", "quantity": "1", "unit": "teaspoon" },
        { "name": "Olive oil", "quantity": "1", "unit": "tablespoon" }
      ],
      "steps": [
        "Preheat the oven to 475°F (245°C).",
        "Roll out the pizza dough on a floured surface to your desired thickness.",
        "Spread pizza sauce evenly over the dough.",
        "Sprinkle mozzarella cheese on top of the sauce.",
        "Distribute mushrooms, bell peppers, red onion, and olives evenly.",
        "Sprinkle Italian seasoning over the vegetables.",
        "Drizzle with olive oil and bake in the oven for 12–15 minutes until the crust is golden and the cheese is melted.",
        "Slice and serve hot."
      ],
      "nutrition": {
        "calories": 250,
        "protein": "10g",
        "fat": "9g",
        "carbohydrates": "30g",
        "fiber": "2g"
      }
    }
  ];
  

  const handleRecipeClick = (recipe) => {
    setSelectedRecipe(selectedRecipe?.recipeName === recipe.recipeName ? null : recipe);
  };

  return (
    <div className="recipe-box">
      {selectedRecipe && (
        <div className="selected-recipe">
          <RecipeCard recipe={selectedRecipe} />
          <button 
            className="close-button"
            onClick={() => setSelectedRecipe(null)}
          >
            Close Recipe
          </button>
        </div>
      )}
      <div className="recipe-grid">
        {recipes.map((recipe, index) => (
          <RecipeTile
            key={index}
            recipe={recipe}
            onClick={() => handleRecipeClick(recipe)}
          />
        ))}
      </div>
    </div>
  );
}

export default RecipeBox;