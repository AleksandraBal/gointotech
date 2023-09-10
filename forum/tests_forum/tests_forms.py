from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import *
from ..forms import *
from datetime import datetime

USER_MODEL = get_user_model()


class TestThreadForm(TestCase):
    """
    Things to test:
    - Are form labels display as expected?
    """
    def test_title_field_label(self):
        form = ThreadForm()
        self.assertEqual(form.fields['title'].label, "")

class TestPostForm(TestCase):
    """
    Things to test:
    - Are form labels display as expected?
    """
    def test_body_field_label(self):
        form = PostForm()
        self.assertEqual(form.fields['body'].label, "")
    
  