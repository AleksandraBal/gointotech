from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
app_name = 'forum'
 
urlpatterns = [
    path('all/', views.thread_list, name='thread_list'),
    path('newthread/', views.add_thread, name='add_thread'),
    path('<int:pk>/', views.thread_detail, name='thread_detail'),
    path('deletethread/<int:pk>/', views.delete_thread, name='delete_thread'),
    path('deletepost/<int:pk>/', views.delete_post, name='delete_post'),
    path('editpost/<int:pk>/', views.edit_post, name='edit_post'),
    path('likepost/<int:pk>/', views.like, name='like'),
]