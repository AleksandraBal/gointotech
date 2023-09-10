from django.contrib import admin
from .models import *

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created']
    list_filter = ['author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ['author']
    date_hierarchy = 'created'
    ordering = ['created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body', 'author', 'article', 'created']
    list_filter = ['author', 'article']
    search_fields = ['body']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created']
