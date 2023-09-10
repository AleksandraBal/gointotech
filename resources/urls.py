from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
app_name = 'resources'
 
urlpatterns = [
    path('all/', views.article_list, name='article_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:article>/', views.article_detail, name='article_detail'),
    path('<int:article_id>/comment/', views.article_comment, name='article_comment'),
    path('add/', views.add_article, name='add_article'),
	path('edit/<int:article_id>/', views.edit_article, name="edit_article"),
	path('delete/<int:article_id>/', views.delete_article, name="delete_article"),
	path('comments/delete/<int:comment_id>/', views.delete_comment, name="delete_comment"),
    path('like/<int:article_id>/', views.like, name='like'),
]