from django.contrib import admin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_ru')
    search_fields = ('title', 'title_ru')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_ru', 'author', 'category', 'pub_date')
    search_fields = ('title', 'title_ru', 'category', 'author')
    raw_id_fields = ('category', 'author')
