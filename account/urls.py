from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
 
urlpatterns = [
  	path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('account/', include('django.contrib.auth.urls')),	
    path('profile/', views.profile, name='profile'),  # user private profile
    path('editprofile/', views.edit_profile, name='edit_profile'), # edit user profile
    path('deleteprofile/', views.delete_profile, name='delete_profile'), # delete user profile
    path('account/<str:username>/', views.user_detail, name='user_detail'), # public profile
    path('all/', views.user_list, name='user_list'),  # display all users
    path('results/', views.search_users, name='search_users'),  
    path('follow/<str:username>/', views.follow, name='follow'), 
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'), 
    path('deletequestion/<int:pk>/', views.delete_question, name='delete_question'),
    path('deleteanswer/<int:pk>/', views.delete_answer, name='delete_answer'),
    path('answer/<int:pk>/', views.answer, name='answer'),
    path('ask/<str:username>/', views.ask, name='ask'), 
]
