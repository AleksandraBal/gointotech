from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..views import *
from ..models import *
from ..urls import *
from ..forms import *
from datetime import datetime

USER_MODEL = get_user_model()

class TestArticletModel(TestCase):
    """
    Things to test:
    - Can you create an article with fields: title, body and author?
    - Does the __str__ method behave as expected?
    - Is a slug automatically created?
    - Is the size of character fields as expected?
    - Does a date get automatically added?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            username='jane',
            password='password123'
        )

        cls.article = Article.objects.create(
            title='My article',
            body='This is my first article',
            author=cls.user,
        )

    def test_create_article(self):
        self.assertEqual(self.article.title, 'My article')
        self.assertEqual(self.article.body, 'This is my first article')
        self.assertEqual(self.article.author, self.user)

 
    def test_title_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)

    def test_article_str(self):
        self.assertEqual(str(self.article), 'My article')

    def test_creates_a_slug(self):
        self.assertEqual(self.article.slug, 'my-article')

    def test_slug_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('slug').max_length
        self.assertEqual(max_length, 250)

    def test_added_date_automatically(self):
        self.assertTrue(type(self.article.created), datetime)

class TestCommenttModel(TestCase):
    """
    Things to test:
    - Can you create a comment with body and author?
    - Does the __str__ method behave as expected?
    - Is the size of character fields as expected?
    - Does a date get automatically added?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            username='jane',
            password='password123'
        )

        cls.article = Article.objects.create(
            title='My article',
            body='This is my first article',
            author=cls.user,
        )

        cls.comment = Comment.objects.create(
            article=cls.article,
            body='This is my first comment',
            author=cls.user,
        )

    def test_create_comment(self):
        self.assertEqual(self.comment.body, 'This is my first comment')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.article, self.article)

    def test_comment_str(self):
        self.assertEqual(str(self.comment), 'This is my first comment')

    def test_body_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('body').max_length
        self.assertEqual(max_length, 2000)

    def test_added_date_automatically(self):
        self.assertTrue(type(self.comment.created), datetime)


class TestLiketModel(TestCase):
    """
    Things to test:
    - Can you create a Like object? 
    - Does the __str__ method behave as expected?
    - Does a date get automatically added?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            username='jane',
            password='password123'
        )

        cls.article = Article.objects.create(
            title='My article',
            body='This is my first article',
            author=cls.user,
        )

        cls.comment = Comment.objects.create(
            article=cls.article,
            body='This is my first comment',
            author=cls.user,
        )

        cls.like = Like.objects.create(
            article=cls.article,
            user=cls.user,
        )

    def test_create_like(self):
        self.assertEqual(self.like.article, self.article)
        self.assertEqual(self.like.user, self.user)

    def test_like_str(self):
        self.assertEqual(str(self.like), 'jane-My article')

    def test_added_date_automatically(self):
        self.assertTrue(type(self.like.created), datetime)

