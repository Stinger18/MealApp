function RecipeItem({ RecipeName, ImageURL }) {
  return (
    <div className="recipe-item">
      <img src={ImageURL} alt={RecipeName + " Image"} className="recipe-img" />
      <h1>{RecipeName}</h1>
    </div>
  );
}

export default RecipeItem;
