import React, { useState } from 'react';
import Comment from './Comment';
import { IComment, IRecipe } from './types';

type voteFn = () => void;

const UpvoteButton: React.FC<{ upvoteFn: voteFn }> = ({ upvoteFn }) => {
  return <button onClick={upvoteFn}>Upvote</button>;
};

const Recipe: React.FC<{recipeInitially: IRecipe}> = ({ recipeInitially }) => {
  const [recipe, setRecipe] = useState<IRecipe>(recipeInitially);
  const upvoteFn: voteFn = () => {
    const refreshRecipe = () => {
      fetch('http://localhost:5000/recipes/' + recipe.id.toString())
        .then(response => response.json())
        .then(response => setRecipe(response['recipe']))
        .catch(error => console.log('ERROR: ' + error.error));
    };
    const doUpvote = () => {
      fetch('http://localhost:5000/recipe/upvote/' + recipe.id.toString(), { method: 'POST' })
        .then(response => refreshRecipe())
        .catch(error => console.log('ERROR: ' + error.error));
    };
    doUpvote();
  };
  return (<div>
    <p><a href={recipe.url}>{recipe.url}</a></p>
    <p><UpvoteButton upvoteFn={upvoteFn} /></p>
    <p>Votes: {recipe.votes}</p>
    {recipe.comments.length > 0 ? <p>Comments:</p> : <></>}
    {recipe.comments.map((comment: IComment) => {
      return <Comment key={comment.id} comment={comment} />;
    })}
  </div>);
};
export default Recipe;
