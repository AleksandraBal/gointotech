from .models import Post, Thread
from django import forms
from django.contrib.auth.models import User

class ThreadForm(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Add a thread title'}))
    class Meta:
        model = Thread
        fields = ['title']

class PostForm(forms.ModelForm):
    body = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Add your post'}))
    class Meta:
        model = Post
        fields = ['body']
        