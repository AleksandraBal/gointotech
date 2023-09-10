from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse
from django.utils.text import slugify

class Article(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    body = models.TextField() 
    author =  models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='articles')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image =  models.ImageField(upload_to='articles/') 
    class Meta:
        ordering = ['-updated', '-created'] 
        indexes = [
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):  
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('resources:article_detail', args=[self.created.year,
                             self.created.month,
                             self.created.day,
                             self.slug])

    def get_like_no(self):
        return self.likes.all().count()

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author =  models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_comments')
    body = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return str(self.body)[:100]

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user =  models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_likes')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + "-" + str(self.article)