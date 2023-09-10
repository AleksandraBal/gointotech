from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..views import *
from ..models import *
from ..urls import *
from ..forms import *
from datetime import datetime

USER_MODEL = get_user_model()

class TestProfiletModel(TestCase):
    """
    Things to test:
    - Can you create a profile?
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

        cls.profile = Profile.objects.create(
            user=cls.user,
            location='Germany',
            bio = "This is a user's bio.",
            current_job = "secretary",
            switching_to = "developer" 
        )

    def test_create_profile(self):
        self.assertEqual(self.profile.bio, "This is a user's bio.")
        self.assertEqual(self.profile.location, 'Germany')
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.current_job, 'secretary')
        self.assertEqual(self.profile.switching_to, 'developer')

    def test_profile_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length_location = profile._meta.get_field('location').max_length
        max_length_current_job = profile._meta.get_field('current_job').max_length
        max_length_switching_to = profile._meta.get_field('switching_to').max_length
        self.assertEqual(max_length_location, 100)
        self.assertEqual(max_length_current_job, 500)
        self.assertEqual(max_length_switching_to, 500)

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'jane')

    def test_added_date_automatically(self):
        self.assertTrue(type(self.profile.created), datetime)

class TestQuestiontModel(TestCase):
    """
    Things to test:
    - Can you create a question?
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
            email='samdoe@test.com',
            first_name='Sam',
            last_name='Doe',
            username='sam',
            password='password123'
        )
        cls.question = Question.objects.create(
            text='This is my first question',
            asker=cls.user1,
            respondent = cls.user2
        )
        cls.answer= Answer.objects.create(
            text='This is my first answer',
            question = cls.question
        )

    def test_create_question(self):
        self.assertEqual(self.question.text, "This is my first question")
        self.assertEqual(self.question.asker, self.user1)
        self.assertEqual(self.question.respondent, self.user2)
    
    def test_create_answer(self):
        self.assertEqual(self.answer.text, "This is my first answer")
        self.assertEqual(self.answer.question, self.question)
 
    def test_question_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('text').max_length
        self.assertEqual(max_length, 1000)

    def test_answer_max_length(self):
        answer = Answer.objects.get(id=1)
        max_length = answer._meta.get_field('text').max_length
        self.assertEqual(max_length, 2000)

    def test_question_str(self):
        self.assertEqual(str(self.question), 'This is my first question')
    
    def test_answer_str(self):
        self.assertEqual(str(self.answer), 'This is my first answer')

    def test_added_date_automatically(self):
        self.assertTrue(type(self.question.posted), datetime)
        self.assertTrue(type(self.answer.posted), datetime)