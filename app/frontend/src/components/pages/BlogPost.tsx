import { usePage } from '@inertiajs/react';

export default function BlogPost() {
  const { props } = usePage();

  const { post } = props;

  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.full_content}</p>
      <small>Category: {post.category}</small>
      <br />
      <small>Author: {post.author}</small>
      <br />
      <small>Date: {post.created_at}</small>
    </div>
  );
}