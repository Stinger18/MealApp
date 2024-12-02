import React from 'react';
import './RecipeCard.css';

function RecipeCard({ recipe }) {
  return (
    <div className="recipe-card">
      <div className="recipe-header">
        <h2>{recipe.recipeName}</h2>
        <p className="description">{recipe.description}</p>
      </div>

      <div className="recipe-meta">
        <div className="time-info">
          <span>Prep: {recipe.prepTime}</span>
          <span>Cook: {recipe.cookTime}</span>
          <span>Total: {recipe.totalTime}</span>
        </div>
        <div className="servings">Servings: {recipe.servings}</div>
      </div>

      <div className="recipe-content">
        <div className="ingredients">
          <h3>Ingredients</h3>
          <ul>
            {recipe.ingredients.map((ingredient, index) => (
              <li key={index}>
                {ingredient.quantity} {ingredient.unit} {ingredient.name}
              </li>
            ))}
          </ul>
        </div>

        <div className="instructions">
          <h3>Instructions</h3>
          <ol>
            {recipe.steps.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ol>
        </div>

        <div className="nutrition">
          <h3>Nutrition Facts</h3>
          <div className="nutrition-grid">
            <span>Calories: {recipe.nutrition.calories}</span>
            <span>Protein: {recipe.nutrition.protein}</span>
            <span>Fat: {recipe.nutrition.fat}</span>
            <span>Carbs: {recipe.nutrition.carbohydrates}</span>
            <span>Fiber: {recipe.nutrition.fiber}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RecipeCard;