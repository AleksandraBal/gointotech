from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics/')
    date_of_birth = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    current_job = models.CharField(blank=True, null=True, max_length=500)
    switching_to = models.CharField(blank=True, null=True, max_length=500)
    location = models.CharField(blank=True, null=True, max_length=100)
    bio = models.TextField(blank=True, null=True)
    career_advice = models.TextField(blank=True, null=True)
    following = models.ManyToManyField("self", blank=True)
    
    
    def __str__(self):
        return str(self.user.username)

    def get_following(self):
        return self.following.all()

    def get_following_no(self):
        return self.following.all().count()


class Question(models.Model):
    asker = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="asked_questions")
    respondent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answered_questions")
    text = models.CharField(max_length=1000)
    posted = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-posted',)
    
    def __str__(self):
        return self.text[:100]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    posted = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-posted',)
    
    def __str__(self):
        return self.text[:100]
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)