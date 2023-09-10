from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
# from ..views import *
from ..models import *
# from ..urls import *
# from ..forms import *
from datetime import datetime

USER_MODEL = get_user_model()


class TestMailThreadtModel(TestCase):
    """
    Things to test:
    - Can you create a thread by specifying sender and receiver?
    - Does the __str__ method behave as expected?
    - Is the size of character fields as expected?
    - Does a date get automatically added?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user1 = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            username='jane',
            password='password123'
        )

        cls.user2 = USER_MODEL.objects.create_user(
            email='sam@test.com',
            first_name='Sam',
            last_name='Doe',
            username='sam',
            password='password123'
        )

        cls.thread = MailThread.objects.create(
            sender = cls.user1,
            receiver = cls.user2
        )

    def test_create_thread(self):
        self.assertEqual(self.thread.sender, self.user1)
        self.assertEqual(self.thread.receiver, self.user2)

    def test_thread_str(self):
        self.assertEqual(str(self.thread), 'jane - sam')


class TestMessagetModel(TestCase):
    """
    Things to test:
    - Can you create a message by specifying thread, body, sender and receiver?
    - Does the __str__ method behave as expected?
    - Is the size of character fields as expected?
    - Does a date get automatically added?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user1 = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            username='jane',
            password='password123'
        )

        cls.user2 = USER_MODEL.objects.create_user(
            email='sam@test.com',
            first_name='Sam',
            last_name='Doe',
            username='sam',
            password='password123'
        )

        cls.thread = MailThread.objects.create(
            sender = cls.user1,
            receiver = cls.user2
        )

        cls.message = Message.objects.create(
            sender_user = cls.user1,
            receiver_user = cls.user2,
            body = 'This is my first message',
            thread = cls.thread,
        )     

    def test_create_messaget(self):
        self.assertEqual(self.message.body, 'This is my first message')
        self.assertEqual(self.message.sender_user, self.user1)
        self.assertEqual(self.message.receiver_user, self.user2)
        self.assertEqual(self.message.thread, self.thread)

    def test_message_str(self):
        self.assertEqual(str(self.message), 'This is my first message')

    def test_body_max_length(self):
        message = Message.objects.get(id=1)
        max_length = message._meta.get_field('body').max_length
        self.assertEqual(max_length, 2000)

    def test_added_date_automatically(self):
        self.assertTrue(type(self.message.sent), datetime)

