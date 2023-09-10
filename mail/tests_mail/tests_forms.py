from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import *
from ..forms import *
from datetime import datetime

USER_MODEL = get_user_model()


class TestMessageForm(TestCase):
    """
    Things to test:
    - Are form fields displayed correctly?
    - Are form labels displayed as expected?
    """
    def test_field_label(self):
        form = MessageForm()
        self.assertEqual(form.fields['body'].label, "")
        self.assertTrue('body' in form.fields)
        self.assertTrue('image' in form.fields)
        self.assertTrue('document' in form.fields)
