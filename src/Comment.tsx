import React from 'react';
import { IComment } from './types';
import moment from 'moment';

const Comment: React.FC<{ comment: IComment }> = ({ comment }) => {
  console.log(comment.posted_at);
  return (
    <div>
      <p>
        {comment.text} - {moment(comment.posted_at).fromNow()}
      </p>
    </div>
  );
};
export default Comment;
