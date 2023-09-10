from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..views import *
from ..models import *
from ..urls import *
from ..forms import *
from datetime import datetime

USER_MODEL = get_user_model()


class TestCommenttForm(TestCase):
    """
    Things to test:
    - Are form labels display as expected?
    """
    def test_body_field_label(self):
        form = CommentForm()
        self.assertEqual(form.fields['body'].label, "")

class TestArticleForm(TestCase):
    """
    Things to test:
    - Are form labels displayed as expected?
    """
    def test_body_field_label(self):
        form = ArticleForm()
        self.assertEqual(form.fields['body'].label, "")
    
    def test_title_field_label(self):
        form = ArticleForm()
        self.assertEqual(form.fields['title'].label, "")

    def test_image_field_label(self):
        form = ArticleForm()
        self.assertEqual(form.fields['image'].label, "Upload an image")