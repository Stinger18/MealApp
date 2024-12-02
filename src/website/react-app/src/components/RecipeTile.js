import React from 'react';
import './RecipeTile.css';

function RecipeTile({ recipe, onClick }) {
  return (
    <div className="recipe-tile" onClick={onClick}>
      <h3>{recipe.recipeName}</h3>
      <p>{recipe.description}</p>
      <div className="recipe-tile-meta">
        <span>🕒 {recipe.totalTime}</span>
        <span>👥 Serves {recipe.servings}</span>
      </div>
    </div>
  );
}

export default RecipeTile;