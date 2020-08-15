import React from 'react';
import { ICategory, IRecipe } from './types';
import Recipe from './Recipe';

const Category: React.FC<{ category: ICategory }> = ({ category }) => {
  return (
    <div>
      <h2>{category.name}</h2>
      {category.recipes.map((recipe: IRecipe) => {
        return <Recipe key={recipe.url} recipeInitially={recipe} />;
      })}
    </div>
  );
};
export default Category;
