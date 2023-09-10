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

class IndexTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/index.html')

class RegisterTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Are the correct form fields displayed?
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

    def test_get_regsiter(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')
        self.assertEqual(reverse("register"), '/register/')

    def test_form_fields(self):
        response = self.client.get(reverse("register"))
        user_form = response.context['user_form']
        self.assertEqual(len(user_form.fields), 6)
        self.assertIn('first_name', user_form.fields)
        self.assertIn('last_name', user_form.fields)
        self.assertIn('email', user_form.fields)
        self.assertIn('username', user_form.fields)
        self.assertIn('password', user_form.fields)
        self.assertIn('password2', user_form.fields)

    def test_post_register(self):
        form_data = {'username':'sam', 'last_name':'Doe', 'first_name': 'Sam', 
                     'password': '1234', 'password2': '1234'}
        response = self.client.post(reverse("register"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register_done.html')
        self.assertEqual(reverse("register"), '/register/')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Profile.objects.count(), 1)

class ProfileTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - If a user isn't logged in, are they redirected?
    - Are the correct form fields displayed?
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
    def test_view_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')
        self.assertEqual(reverse("profile"), '/profile/')

    def test_edit_profile_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("edit_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/edit.html')
        self.assertEqual(reverse("edit_profile"), '/editprofile/')
    
    def test_edit_profile_post(self):
        self.client.force_login(self.user)
        self.url = reverse('edit_profile')
        form_data = {'location':'France'}
        self.profile.location = form_data["location"]
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(self.profile.location, 'France')

    def test_delete_profile(self):
        self.client.force_login(self.user)
        self.url = reverse('delete_profile')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.profile.delete()
        self.user.delete()
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)

class PublicProfileTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - If a user isn't logged in, are they redirected?
    - Are the correct form fields displayed?
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
    def test_view_public_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("user_detail", args=['jane']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse("profile"), '/profile/')

class QuestionAnswerTest(TestCase):
    """ Things to test:
    - Can the user create questions and answers?
    - Can the user delete questions and answers?
    - Is the right response code returned?
    - Does the user get redirected to the right page?
    """
    @classmethod
    @freeze_time("2012-10-10")
    def setUpTestData(cls):
        cls.client = Client()
        
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
        cls.profile1 = Profile.objects.create(
            user = cls.user1
        )
        cls.profile2 = Profile.objects.create(
            user = cls.user2
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
    def test_read_question(self):
        self.client.force_login(self.user1)
        self.assertEqual(self.question.asker, self.user1)
        self.assertEqual(self.question.respondent, self.user2)
        self.assertEqual(self.question.text, 'This is my first question')
    
    def test_read_answer(self):
        self.client.force_login(self.user1)
        self.assertEqual(self.answer.question, self.question)
        self.assertEqual(self.answer.text, 'This is my first answer')
    
    def test_delete_answer(self):
        self.client.force_login(self.user2)
        self.url = reverse('delete_answer', args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,(reverse('profile')))
        self.answer.delete()
        self.assertEqual(Answer.objects.count(), 0)
    
    def test_delete_question(self):
        self.client.force_login(self.user1)
        self.url = reverse('delete_question', args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_detail', args=['sam']))
        self.question.delete()
        self.assertEqual(Question.objects.count(), 0)

class UserListTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Is the right response code returned?
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
            user = cls.user
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/all/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user_list.html')

class FollowTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Is the right response code returned?
    """
    @classmethod
    @freeze_time("2012-10-10")
    def setUpTestData(cls):
        cls.client = Client()
        
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
        cls.profile1 = Profile.objects.create(
            user = cls.user1
        )
        cls.profile2 = Profile.objects.create(
            user = cls.user2
        )
    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user1)
        response = self.client.get('/follow/sam/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('follow', args=['sam']))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('follow', args=['sam']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/follow.html')

class UnfollowTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Is the right response code returned?
    """
    @classmethod
    @freeze_time("2012-10-10")
    def setUpTestData(cls):
        cls.client = Client()
        
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
        cls.profile1 = Profile.objects.create(
            user = cls.user1
        )
        cls.profile2 = Profile.objects.create(
            user = cls.user2
        )
    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user1)
        response = self.client.get('/unfollow/sam/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('unfollow', args=['sam']))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('unfollow', args=['sam']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/unfollow.html')