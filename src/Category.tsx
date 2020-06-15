import React from 'react';
import { Card } from 'antd';
import { ICategory, IRecipe } from './types';
import Recipe from './Recipe';

const Category: React.FC<{category: ICategory}> = ({ category }) => {
  return (<Card>
    <h2>{category.name}</h2>
    {category.recipes.map((recipe: IRecipe) => {
      return <Recipe key={recipe.url} recipe={recipe} />;
    })}
  </Card>);
};
export default Category;
