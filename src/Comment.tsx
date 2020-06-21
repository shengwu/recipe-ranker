import React from 'react';
import { IComment } from './types';
import moment from 'moment';

const Comment: React.FC<{comment: IComment}> = ({ comment }) => {
  return (<div>
    <p>{comment.text}</p>
    <p>{moment(comment.posted_at).format('h:mm a - ddd MMMM Do YYYY')}</p>
  </div>);
};
export default Comment;
