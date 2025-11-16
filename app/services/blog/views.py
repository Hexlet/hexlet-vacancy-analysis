from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import View
from inertia import render as inertia_render

from .models import BlogCategory, BlogPost, Tag

User = get_user_model()


class BlogListView(View):
    def get(self, request):
        qs = BlogPost.objects.select_related(
            'category', 'author').prefetch_related('tags')

        category_id = request.GET.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)

        q = request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(content_full__icontains=q)
            )

        paginator = Paginator(qs, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        posts = list(page_obj.object_list.values(
            'id', 'title', 'content_short', 'content_full',
            'category__name', 'author__first_name', 'created_at',
            'is_published', 'duration_minutes'
        ))

        categories = list(BlogCategory.objects.values('id', 'name'))
        users = list(User.objects.values('id', 'first_name'))
        tags = list(Tag.objects.values('id', 'name'))

        return inertia_render(
            request,
            "Blog",
            props={
                'posts': posts,
                'categories': categories,
                'users': users,
                'tags': tags,
                'pagination': {
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'current_page': page_obj.number,
                    'num_pages': paginator.num_pages,
                },
                'filter': {
                    'category': category_id,
                    'q': q,
                }
            }
        )


class BlogDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        post_data = {
            'id': post.id,
            'title': post.title,
            'content_short': post.content_short,
            'content_full': post.content_full,
            'created_at': post.created_at,
            'is_published': post.is_published,
            'duration_minutes': post.duration_minutes,
            'category': post.category.name,
            'author': post.author.email,
            'tags': list(post.tags.values_list('name', flat=True)),
        }
        return inertia_render(request, "BlogPost", props={'post': post_data})
