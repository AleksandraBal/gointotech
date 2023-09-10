from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms.widgets import NumberInput, TextInput


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Profile
        fields = ['image', 'current_job', 'switching_to','bio', 'location', 'career_advice','date_of_birth']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]
        widgets = {
            'text': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Ask a question'
                })
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text"]
        widgets = {
            'text': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Answer here'
                })
        }