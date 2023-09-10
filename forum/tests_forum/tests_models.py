from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import *
from datetime import datetime

USER_MODEL = get_user_model()

class TestThreadtModel(TestCase):
    """
    Things to test:
    - Can you create a thread by specifying title and author?
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

        cls.thread = Thread.objects.create(
            title='My thread',
            author=cls.user
        )

    def test_create_thread(self):
        self.assertEqual(self.thread.title, 'My thread')
        self.assertEqual(self.thread.author, self.user)
 
    def test_title_max_length(self):
        thread = Thread.objects.get(id=1)
        max_length = thread._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)

    def test_thread_str(self):
        self.assertEqual(str(self.thread), 'My thread')

    def test_added_date_automatically(self):
        self.assertTrue(type(self.thread.created), datetime)

class TestPosttModel(TestCase):
    """
    Things to test:
    - Can you create a post by specifying thread, body and author?
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
        
        cls.thread = Thread.objects.create(
            title='My thread',
            author=cls.user
        )

        cls.post = Post.objects.create(
            thread=cls.thread,
            body='This is my first post',
            author=cls.user,
        )

    def test_create_post(self):
        self.assertEqual(self.post.body, 'This is my first post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.thread, self.thread)

    def test_post_str(self):
        self.assertEqual(str(self.post), 'This is my first post')

    def test_body_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('body').max_length
        self.assertEqual(max_length, 2000)

    def test_added_date_automatically(self):
        self.assertTrue(type(self.post.created), datetime)

class TestPostLikeModel(TestCase):
    """
    Things to test:
    - Can you create a PostLike object? 
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
        
        cls.thread = Thread.objects.create(
            title='My thread',
            author=cls.user
        )

        cls.post = Post.objects.create(
            thread=cls.thread,
            body='This is my first post',
            author=cls.user,
        )
        cls.like = PostLike.objects.create(
            post=cls.post,
            user=cls.user,
        )

    def test_create_like(self):
        self.assertEqual(self.like.post, self.post)
        self.assertEqual(self.like.user, self.user)

    def test_like_str(self):
        self.assertEqual(str(self.like), 'jane likes This is my first post')

    def test_added_date_automatically(self):
        self.assertTrue(type(self.like.created), datetime)

