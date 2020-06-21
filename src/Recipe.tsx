import React, { useState } from 'react';
import Comment from './Comment';
import { Input, Button, Card } from 'antd';
import { IComment, IRecipe } from './types';
import { css } from '@emotion/core';

const recipeStyle = css({
  marginBottom: '10px',
})

type submitFn = (event: any) => void;
type voidFn = () => void;


const CommentForm: React.FC<{recipe: IRecipe, refreshRecipe: voidFn}> = ({ recipe, refreshRecipe }) => {
  const submitComment: submitFn = (event: any) => {
    const comment = {
      recipe_id: recipe.id,
      text: event.target.value,
    }
    const postComment = (commentFields: object) => {
      fetch('http://localhost:5000/comments', { method: 'POST', body: JSON.stringify(commentFields), headers: { 'Content-Type': 'application/json' }})
        .then(response => refreshRecipe())
        .catch(error => console.log('ERROR: ' + error));
    };
    postComment(comment);
  };
  return <Input placeholder='Enter a comment..' onPressEnter={submitComment} />
};

const Recipe: React.FC<{recipeInitially: IRecipe}> = ({ recipeInitially }) => {
  const [recipe, setRecipe] = useState<IRecipe>(recipeInitially);
  const refreshRecipe = () => {
    fetch('http://localhost:5000/recipes/' + recipe.id.toString())
      .then(response => response.json())
      .then(response => setRecipe(response['recipe']))
      .catch(error => console.log('ERROR: ' + error.error));
  };
  const upvoteFn: voidFn = () => {
    const doUpvote = () => {
      fetch('http://localhost:5000/recipe/upvote/' + recipe.id.toString(), { method: 'POST' })
        .then(response => refreshRecipe())
        .catch(error => console.log('ERROR: ' + error.error));
    };
    doUpvote();
  };
  return (<Card css={recipeStyle}>
    <p><a href={recipe.url}>{recipe.url}</a></p>
    <Button onClick={upvoteFn}>Upvote</Button>
    <p>Votes: {recipe.votes}</p>
    {recipe.comments.length > 0 ? <p>Comments:</p> : <></>}
    {recipe.comments.map((comment: IComment) => {
      return <Comment key={comment.id} comment={comment} />;
    })}
    <CommentForm recipe={recipe} refreshRecipe={refreshRecipe} />
  </Card>);
};
export default Recipe;
