from .models import Comment, Article
from django import forms
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels ={"body": ""}

class ArticleForm(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Article title'}))
    body = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Write your article here'}))
    image =  forms.ImageField(label="Upload an image")
    class Meta:
        model = Article
        fields = ['title', 'body', 'image']
    