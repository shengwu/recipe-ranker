import React, { useState } from 'react';
import { Input } from 'antd';
import { IRecipe } from './types';

type voidFn = () => void;

const CommentForm: React.FC<{
  recipe: IRecipe;
  refreshRecipe: voidFn;
}> = ({ recipe, refreshRecipe }) => {
  const [comment, setComment] = useState<string>('');
  const submitComment: voidFn = () => {
    if (comment.trim() === '') {
      return;
    }
    const commentParams = {
      recipe_id: recipe.id,
      text: comment.trim(),
    };
    const postComment = (commentFields: object): void => {
      fetch('http://localhost:5000/comments', {
        method: 'POST',
        body: JSON.stringify(commentFields),
        headers: { 'Content-Type': 'application/json' },
      })
        .then(() => {
          setComment('');
          refreshRecipe();
        })
        .catch((error) => console.log('ERROR: ' + error));
    };
    postComment(commentParams);
  };
  return (
    <Input
      placeholder="Enter a comment.."
      value={comment}
      onChange={(e): void => setComment(e.target.value)}
      onPressEnter={submitComment}
    />
  );
};

export default CommentForm;
