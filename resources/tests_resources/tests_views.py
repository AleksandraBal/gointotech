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

class ArticleListTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Does the pagination work correctly?
    - Are the right status codes returned?
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
        # Create 12 authors for pagination tests
        number_of_articles = 12

        for article_id in range(number_of_articles):
            Article.objects.create(
                title=f'Article title {article_id}',
                body=f'Article text {article_id}',
                author=cls.user,
                image = tempfile.NamedTemporaryFile(suffix=".jpg").name
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/resources/all/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('resources:article_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('resources:article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/article_list.html')

    def test_pagination_is_three(self):
        response = self.client.get(reverse('resources:article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 3)

    def test_pagination_last_page(self):
        # Get last page and confirm it has also 3 items
        response = self.client.get(reverse('resources:article_list')+'?page=4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 3)

class ArticleDetailTest(TestCase):
    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - Are the right status codes returned?
    - Are the existing instances of article, comment and like displayed?
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
        
        cls.article = Article.objects.create(
            title='My article',
            body='This is my first article',
            author=cls.user,
            image = tempfile.NamedTemporaryFile(suffix=".jpg").name,
            created = datetime.now()
        )

        cls.comment = Comment.objects.create(author=cls.user, 
                                created = datetime.now(),
                                article = cls.article,
                                body = "text")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/resources/2012/10/10/my-article/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('resources:article_detail', args=[2012,10,10,'my-article']))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('resources:article_detail', args=[2012,10,10,'my-article']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/article.html')
    
    def test_read_article(self):
        self.assertEqual(self.article.author, self.user)
        self.assertEqual(self.article.body, 'This is my first article')
        self.assertEqual(self.article.title, 'My article')
        self.assertEqual(self.article.slug, 'my-article')
    
    def test_read_comment(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.body, 'text')
        self.assertEqual(self.comment.article, self.article)
    
    def test_like(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('resources:like', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('resources:article_detail', args=[2012,10,10,'my-article']))

class TestAddArticle(TestCase):

    """ Things to test:
    - Does a specific URL exist?
    - Does a URL get generated from its name in the URL configuration?
    - Is the correct template used?
    - If a user isn't logged in, are they redirected?
    - Are the correct form fields displayed?
    - Are the right status codes returned?
    - Is the user able to add an article and upload an image?
    - Is the user redirected to the right pages?
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('resources:add_article')
        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            username='jane',
            password='password4123'
        )

    def test_get_add(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/add_article.html')
        self.assertEqual(self.url, '/resources/add/')

    def test_user_must_be_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_form_fields(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        form = response.context['form']

        self.assertEqual(len(form.fields), 3)
        self.assertIn('title', form.fields)
        self.assertIn('body', form.fields)
        self.assertIn('image', form.fields)

    def test_post_add(self):
        self.client.force_login(self.user)
        form_data = {'title':'new title', 'body':'my new article', 'image': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('resources:article_list'))

class TestAddComment(TestCase):

    """ Things to test:
    - Does submitting a comment redirects to the expected URL?
    - Are the right status codes returned?
    - Is the user able to create a comment?
    """

    @classmethod
    @freeze_time("2012-10-10")
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('resources:article_comment', args=[1])
        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            username='jane',
            password='password123'
        )
        
        cls.article = Article.objects.create(
            title='My article',
            body='This is my first article',
            author=cls.user,
            image = tempfile.NamedTemporaryFile(suffix=".jpg").name,
            created = datetime.now()
        )
    
    def test_comment_add(self):
        self.client.force_login(self.user)
        form_data = {'body':'my new comment'}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('resources:article_detail', args=[2012,10,10,'my-article']))
        self.assertEqual(Comment.objects.count(), 1)

class TestModifyArticleComment(TestCase):

    """ Things to test:
        - Does a specific URL exist?
        - Does a URL get generated from its name in the URL configuration?
        - Is the correct template used?
        - If a user isn't logged in, are they redirected?
        - Are the right status codes returned?
        - Is the user able to edit an article?
        - Is the user able to delete an article and comment?
        - Is the user redirected to the right pages?
    """
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
        
        cls.article = Article.objects.create(
            title='My article',
            body='This is my first article',
            author=cls.user,
            image = tempfile.NamedTemporaryFile(suffix=".jpg").name,
            created = datetime.now()
        )

        cls.comment = Comment.objects.create(author=cls.user, 
                                created = datetime.now(),
                                article = cls.article,
                                body = "text")
      
    def test_edit_article_get(self):
        self.client.force_login(self.user)
        response = self.client.get('/resources/edit/1/')
        self.assertTemplateUsed(response, 'resources/edit_article.html')
        self.assertEqual(response.status_code, 200)

    def test_edit_article_post(self):
        self.client.force_login(self.user)
        self.url = reverse('resources:edit_article', args=[1])
        form_data = {'body':'new content'}
        self.article.body = form_data["body"]
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('resources:article_list'))
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(self.article.body, 'new content')
    
    def test_delete_comment(self):
        self.client.force_login(self.user)
        self.url = reverse('resources:delete_comment', args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,(reverse('resources:article_detail', args=[2012,10,10,'my-article'])))
        self.comment.delete()
        self.assertEqual(Comment.objects.count(), 0)
    
    def test_delete_article(self):
        self.client.force_login(self.user)
        self.url = reverse('resources:delete_article', args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('resources:article_list'))
        self.article.delete()
        self.assertEqual(Article.objects.count(), 0)


    