from django.contrib import admin

from .models import Category, Genre, Comment, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий произведений."""

    list_display = ['pk', 'name', 'slug']
    search_fields = ['name']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка для произведений."""

    list_display = ['pk', 'name', 'year', 'category']
    search_fields = ['year', 'category__name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для жанра произведений."""

    list_display = ['pk', 'name', 'slug']
    search_fields = ['name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для отзывов."""

    list_display = ('pk', 'title', 'pub_date', 'author', 'text', 'score')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев."""

    list_display = ('pk', 'review', 'author', 'pub_date', 'text')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
