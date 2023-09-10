from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
 
urlpatterns = [
    path('mailbox/', views.mailbox, name='mailbox'),
    path('thread/<str:username>/', views.thread, name='thread'),
    path('deletethread/<int:pk>/', views.delete_thread, name='delete_thread'),
    path('thread/<int:pk>/new_message/', views.new_message, name='new_message'),
    path('deletemessage/<int:pk>/', views.delete_message, name='delete_message'),
]