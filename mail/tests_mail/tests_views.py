from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..views import *
from ..models import *
from ..urls import *
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from freezegun import freeze_time
from datetime import datetime

USER_MODEL = get_user_model()

class MailboxTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Does the pagination work correctly?
    - Are the existing threads displayed?
    - Are the right status codes returned?
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

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user1)
        response = self.client.get('/mail/mailbox/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('mailbox'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('mailbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mail/mailbox.html')

class ThreadDetailTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Are the existing messages displayed?
    - Are the right status codes returned?
    """
    
    @classmethod
    @freeze_time("2012-10-10")
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

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user1)
        response = self.client.get('/mail/thread/sam/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('thread', args=['sam']))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('thread', args=['sam']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mail/thread.html')
    
    def test_read_thread(self):
        self.client.force_login(self.user1)
        self.assertEqual(self.thread.sender, self.user1)
        self.assertEqual(self.thread.receiver, self.user2)
    
    def test_read_message(self):
        self.client.force_login(self.user1)
        self.assertEqual(self.message.sender_user, self.user1)
        self.assertEqual(self.message.receiver_user, self.user2)
        self.assertEqual(self.message.body, 'This is my first message')
        self.assertEqual(self.message.thread, self.thread)
    
    def test_form_fields(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('thread', args=['sam']))
        form = response.context['form']
        self.assertEqual(len(form.fields), 3)
        self.assertIn('body', form.fields)
        self.assertIn('image', form.fields)
        self.assertIn('document', form.fields)


class DeleteThreadAndMessage(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Does the message and thread get deleted?
    - Are the right status codes returned?
    - Is the user redirected to the right page?
    """

    @classmethod
    @freeze_time("2012-10-10")
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

    
    def test_delete_message(self):
        self.client.force_login(self.user1)
        self.url = reverse('delete_message', args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,(reverse('thread', args=['sam'])))
        self.message.delete()
        self.assertEqual(Message.objects.count(), 0)
    
    def test_delete_thread(self):
        self.client.force_login(self.user1)
        self.url = reverse('delete_thread', args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mailbox'))
        self.thread.delete()
        self.assertEqual(MailThread.objects.count(), 0)


class NewMessage(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - If a user isn't logged in, are they redirected?
    - Are the correct form fields displayed?
    - Does a message get created?
    - Are the right status codes returned?
    - Is the user redirected to the right pages?
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

    def test_user_must_be_logged_in(self):
        response = self.client.post(reverse('new_message', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_message_add(self):
        self.client.force_login(self.user1)
        form_data = {'body':'my new message'}
        response = self.client.post(reverse('new_message', args=[1]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,(reverse('thread', args=['sam'])))