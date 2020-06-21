import React from 'react';
import { IComment } from './types';
//import moment from 'moment';

const Comment: React.FC<{comment: IComment}> = ({ comment }) => {
  return (<div>
    <p>{comment.text} - {new Date(comment.posted_at).toString()}</p>
  </div>);
};
export default Comment;
