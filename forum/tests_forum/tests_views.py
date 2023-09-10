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

class ThreadListTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Does the pagination work correctly?
    - Does the correct thread titles are displayed?
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
        # Create 12 threads for pagination tests
        number_of_threads = 12
        cls.threads = []
        for thread_id in range(number_of_threads):    
            thread = Thread.objects.create(
                title=f'Thread title {thread_id}',
                author=cls.user
            )
            cls.threads.append(thread)

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/forum/all/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:thread_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('resources:article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/article_list.html')

    def test_pagination_is_ten(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:thread_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['threads']), 10)

    def test_pagination_last_page(self):
        # Get last page and confirm it has 2 items
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:thread_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['threads']), 2)
    
    def test_read_thread(self):
        self.assertEqual(self.threads[1].author, self.user)
        self.assertEqual(self.threads[1].title, 'Thread title 1')

class ThreadDetailTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Does the thread dispay its title and posts?
    """
    
    @classmethod
    @freeze_time("2012-10-10")
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
            author=cls.user,
            created = datetime.now()
        )

        cls.post = Post.objects.create(author=cls.user, 
                                created = datetime.now(),
                                thread = cls.thread,
                                body = "post")

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/forum/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:thread_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:thread_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/thread_detail.html')
    
    def test_read_thread(self):
        self.client.force_login(self.user)
        self.assertEqual(self.thread.author, self.user)
        self.assertEqual(self.thread.title, 'My thread')
    
    def test_read_post(self):
        self.client.force_login(self.user)
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.body, 'post')
        self.assertEqual(self.post.thread, self.thread)

    def test_like(self):
        self.client.force_login(self.user)
        self.url = reverse('forum:like', args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,(reverse('forum:thread_detail', args=[1])))

class AddThread(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - If a user isn't logged in, are they redirected?
    - Are the correct form fields displayed?
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('forum:add_thread')
        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            username='jane',
            password='password4123'
        )

    def test_user_must_be_logged_in(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_add(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/add_thread.html')
        self.assertEqual(self.url, '/forum/newthread/')

    def test_form_fields(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        thread_form = response.context['thread_form']
        self.assertEqual(len(thread_form.fields), 1)
        self.assertIn('title', thread_form.fields)
        post_form = response.context['post_form']
        self.assertEqual(len(post_form.fields), 1)
        self.assertIn('body', post_form.fields)


    def test_thread_add(self):
        self.client.force_login(self.user)
        form_data = {'title':'new thread', 'body':'my new post'}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('forum:thread_list'))



class ModifyPostAndThread(TestCase):

    @classmethod
    @freeze_time("2012-10-10")
    def setUpTestData(cls):
        cls.client = Client()
        
        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            username='jane',
            password='password123'
        )
        
        cls.thread = Thread.objects.create(
            title='My thread',
            author=cls.user,
            created = datetime.now()
        )

        cls.post = Post.objects.create(author=cls.user, 
                                created = datetime.now(),
                                thread = cls.thread,
                                body = "post")
      
    def test_edit_post_get(self):
        self.client.force_login(self.user)
        response = self.client.get('/forum/editpost/1/')
        self.assertTemplateUsed(response, 'forum/edit_post.html')
        self.assertEqual(response.status_code, 200)

    def test_edit_post_post(self):
        self.client.force_login(self.user)
        self.url = reverse('forum:edit_post', args=[1])
        form_data = {'body':'new content'}
        self.post.body = form_data["body"]
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('forum:thread_detail', args=[1]))
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.body, 'new content')

    
    def test_delete_post(self):
        self.client.force_login(self.user)
        self.url = reverse('forum:delete_post', args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,(reverse('forum:thread_detail', args=[1])))
        self.post.delete()
        self.assertEqual(Post.objects.count(), 0)
    
    def test_delete_thread(self):
        self.client.force_login(self.user)
        self.url = reverse('forum:delete_thread', args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('forum:thread_list'))
        self.thread.delete()
        self.assertEqual(Thread.objects.count(), 0)

 

