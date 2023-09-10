from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from resources.api import serializers
from ..models import *


class ArticleTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", 
                                             password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.article = Article.objects.create(title='My article', 
                                              body='This is my first article', 
                                              author=self.user)

    def test_article_create(self):
        data = {
            "title": 'My new article', 
            "body": 'This is my new article', 
            "author": self.user
        }
        response = self.client.post(reverse('api_article_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_article_create_unauth(self):
        data = {
            "title": 'My new article', 
            "body": 'This is my new article', 
            "author": self.user
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('api_article_create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_article_list(self):
        response = self.client.get(reverse('api_article_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_article_detail(self):
        response = self.client.get(reverse('api_article_detail', 
                                           args=(self.article.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().body, 'This is my first article')
        self.assertEqual(Article.objects.get().title, 'My article')

    def test_article_update(self):
        data = {
            "title": 'My article', 
            "body": 'updated body', 
            "author": self.user
        }
        response = self.client.put(reverse('api_article_detail', 
                                           args=(self.article.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.get().body, 'updated body')
    
    def test_article_delete(self):
        response = self.client.delete(reverse('api_article_detail', 
                                              args=(self.article.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CommentTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.article = Article.objects.create(title='My article', 
                                              body='This is my first article', 
                                              author=self.user)
        self.comment = Comment.objects.create(article = self.article, 
                                              author=self.user, 
                                              body = "This is a comment")

    def test_comment_create(self):
        data = {
            "article": self.article,
            "author": self.user,
            "body": "This is a new comment"
        }
        response = self.client.post(reverse('api_comment_add', 
                                            args=(self.article.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_comment_create_unauth(self):
        data = {
            "article": self.article,
            "author": self.user,
            "body": "This is a new comment"
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('api_comment_add', 
                                            args=(self.article.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_list(self):
        response = self.client.get(reverse('api_comment_list', 
                                           args=(self.article.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_comment_detail(self):
        response = self.client.get(reverse('api_comment_detail', 
                                           args=(self.comment.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().body, 'This is a comment')
    
    def test_comment_update(self):
        data = {
            "body": "new text",
            "article": self.article,
            "author": self.user
        }
        response = self.client.put(reverse('api_comment_detail', 
                                           args=(self.comment.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get().body, 'new text')
    
    def test_comment_delete(self):
        response = self.client.delete(reverse('api_comment_detail', 
                                              args=(self.comment.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LikeTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", 
                                             password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.article = Article.objects.create(title='My article', 
                                              body='This is my first article', 
                                              author=self.user)
        self.like = Like.objects.create(article=self.article, user=self.user)
    
    def test_like(self):
        response = self.client.get(reverse('api_like', args=(self.article.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 1)
        
