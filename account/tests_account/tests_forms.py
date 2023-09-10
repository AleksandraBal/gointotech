from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import *
from ..forms import *
from datetime import datetime

USER_MODEL = get_user_model()


class TestQuestionForm(TestCase):
    """
    Things to test:
    - Are form labels display as expected?
    """
    def test_text_field_label(self):
        form = QuestionForm()
        self.assertEqual(form.fields['text'].label, "Text")

class TestAnswerForm(TestCase):
    """
    Things to test:
    - Are form labels display as expected?
    """
    def test_text_field_label(self):
        form = AnswerForm()
        self.assertEqual(form.fields['text'].label, "Text")

class TestUserEditForm(TestCase):
    """
    Things to test:
    - Are form labels display as expected?
    """
    def test_field_label(self):
        form = UserEditForm()
        self.assertEqual(form.fields['first_name'].label, "First name")
        self.assertEqual(form.fields['last_name'].label, "Last name")
        self.assertEqual(form.fields['email'].label, "Email address")

class TestProfileEditForm(TestCase):
    """
    Things to test:
    - Are form labels display as expected?
    """
    def test_field_label(self):
        form = ProfileEditForm()
        self.assertEqual(form.fields['location'].label, "Location")
        self.assertEqual(form.fields['current_job'].label, "Current job")
        self.assertEqual(form.fields['switching_to'].label, "Switching to")
        self.assertEqual(form.fields['image'].label, "Image")
        self.assertEqual(form.fields['bio'].label, "Bio")
        self.assertEqual(form.fields['career_advice'].label, "Career advice")

class TestUserRegsitrationForm(TestCase):
    """
    Things to test:
    - Are form labels display as expected?
    """
    def test_field_label(self):
        form = UserRegistrationForm()
        self.assertEqual(form.fields['password'].label, "Password")
        self.assertEqual(form.fields['password2'].label, "Repeat password")
