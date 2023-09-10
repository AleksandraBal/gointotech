from django.urls import path
from . import views
 
urlpatterns = [
  	path('articles/', views.ArticleList.as_view(), name='api_article_list'),
    path('article/<int:pk>/', views.ArticleDetail.as_view(), name='api_article_detail'),
    path('articlecreate/', views.ArticleCreate.as_view(), name='api_article_create'),
    path('<int:pk>/comments/', views.CommentList.as_view(), name='api_comment_list'),
    path('<int:pk>/addcomment/', views.CommentAdd.as_view(), name='api_comment_add'),
    path('comment/<int:pk>/', views.CommentDetail.as_view(), name='api_comment_detail'),
    path('<int:pk>/like/', views.Like.as_view(), name='api_like'),
]   