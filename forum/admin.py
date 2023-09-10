from django.contrib import admin
from .models import *

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created']
    list_filter = ['author']
    date_hierarchy = 'created'
    ordering = ['created']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['body', 'author', 'thread', 'created']
    list_filter = ['author', 'thread']

    