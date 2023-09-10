from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse

class Thread(models.Model):
    title = models.CharField(max_length=250)
    author =  models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created'] 
        indexes = [
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_post_no(self):
        return self.posts.all().count()
    
    def get_last_post(self):
        return self.posts.latest('created')

    def get_last_post_date(self):
        last_post = self.posts.latest('created')
        return last_post.created

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    author =  models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_posts')
    body = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return str(self.body)[:100]
    
    def get_like_no(self):
        return self.post_likes.all().count()

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user =  models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " likes " + str(self.post.body)[:30]