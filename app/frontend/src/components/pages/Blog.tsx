import { usePage } from '@inertiajs/react';
import { Link } from '@inertiajs/react';

export default function Blog() {
  const { props } = usePage();
  console.log('Props from server:', props); // ← добавьте эту строку

  const { posts, categories, pagination, filter } = props;

  const handleCategoryChange = (e) => {
    const categoryId = e.target.value;
    const params = new URLSearchParams(window.location.search);
    if (categoryId) {
      params.set('category', categoryId);
    } else {
      params.delete('category');
    }
    window.location.search = params.toString();
  };

  const handleSearch = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const q = formData.get('q');
    const params = new URLSearchParams(window.location.search);
    if (q) {
      params.set('q', q);
    } else {
      params.delete('q');
    }
    window.location.search = params.toString();
  };

  return (
    <div>
      <h1>Blog Articles</h1>
      <form onSubmit={handleSearch} style={{ marginBottom: '1em' }}>
        <select defaultValue={filter.category || ''} onChange={handleCategoryChange}>
          <option value=''>All categories</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
        <input type="text" name="q" defaultValue={filter.q || ''} placeholder="Search..." />
        <button type="submit">Search</button>
      </form>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <Link href={`/blog/${post.id}`}>
              <h2>{post.title}</h2>
            </Link>
            <p>{post.short_content}</p>
            <small>Category: {post.category}</small>
            <br />
            <small>Author: {post.author}</small>
          </li>
        ))}
      </ul>
      <div>
        {pagination.has_previous && (
          <Link href={`?page=${pagination.current_page - 1}`}>Previous</Link>
        )}
        <span>
          Page {pagination.current_page} of {pagination.num_pages}
        </span>
        {pagination.has_next && (
          <Link href={`?page=${pagination.current_page + 1}`}>Next</Link>
        )}
      </div>
    </div>
  );
}