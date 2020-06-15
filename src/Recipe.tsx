import React from 'react';
import { IRecipe } from './types';

const Recipe: React.FC<{recipe: IRecipe}> = ({ recipe }) => {
  return (<div>
    <p><a href={recipe.url}>{recipe.url}</a></p>
    <p>Votes: {recipe.votes}</p>
  </div>);
};
export default Recipe;
