from __future__ import annotations

from uuid import UUID

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from django.db.models import Q

from .models import Post, Category


def search_posts(query: str) -> QuerySet:
    """Search posts by query in title, category and author"""
    return Post.objects.filter(
        Q(title__icontains=query) | Q(title_ru__icontains=query) |
        Q(category__title__icontains=query) |
        Q(category__title_ru__icontains=query) |
        Q(author__username__icontains=query)
    )


def get_category_posts(category_pk: UUID) -> tuple:
    """Return tuple with category and category posts"""
    category = get_object_or_404(Category, pk=category_pk)
    posts = category.posts.all()
    return category, posts
