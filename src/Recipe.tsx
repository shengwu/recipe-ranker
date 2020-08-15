import React, { useState } from 'react';
import Comment from './Comment';
import CommentForm from './CommentForm';
import { Button, Card } from 'antd';
import { IComment, IRecipe } from './types';
import { css } from '@emotion/core';

const recipeStyle = css({
  marginBottom: '10px',
});

type voidFn = () => void;

interface RecipeProps {
  recipeInitially: IRecipe;
}

const Recipe: React.FC<RecipeProps> = ({ recipeInitially }) => {
  const [recipe, setRecipe] = useState<IRecipe>(recipeInitially);
  const refreshRecipe = (): void => {
    fetch('http://localhost:5000/recipes/' + recipe.id.toString())
      .then((response) => response.json())
      .then((response) => setRecipe(response['recipe']))
      .catch((error) => console.log('ERROR: ' + error.error));
  };
  const upvoteFn: voidFn = () => {
    const doUpvote = (): void => {
      fetch('http://localhost:5000/recipe/upvote/' + recipe.id.toString(), { method: 'POST' })
        .then(() => refreshRecipe())
        .catch((error) => console.log('ERROR: ' + error.error));
    };
    doUpvote();
  };
  return (
    <Card css={recipeStyle}>
      <p>
        <a href={recipe.url}>{recipe.url}</a>
      </p>
      <Button onClick={upvoteFn}>Upvote</Button>
      <p>Votes: {recipe.votes}</p>
      {recipe.comments.length > 0 ? <p>Comments:</p> : <></>}
      {recipe.comments.map((comment: IComment) => {
        return <Comment key={comment.id} comment={comment} />;
      })}
      <CommentForm recipe={recipe} refreshRecipe={refreshRecipe} />
    </Card>
  );
};

export default Recipe;
