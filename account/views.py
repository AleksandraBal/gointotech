from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import *
from django.db.models import Q
from actions.utils import create_action

def index(request):
    return render(request, "account/index.html")

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

# Display a private profile
@login_required
def profile(request): 
    form = AnswerForm()
    questions = Question.objects.filter(respondent=request.user)
    answers = Answer.objects.all()
    number_followers = request.user.profile.following.all().count()
    context = {"number_followers": number_followers, "questions": questions, "answers": answers, "form": form}
    return render(request, 'account/profile.html', context)

# Edit profile
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            username = user_form.cleaned_data.get("username")
            create_action(request.user, 'updated profile')
        return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/edit.html', {'user_form': user_form,
                   'profile_form': profile_form})

# Display a public profile
@login_required
def user_detail(request, username):
    if request.method == 'GET':
        other_user = get_object_or_404(User, username=username)
        form = QuestionForm()
        if other_user == request.user:
            return redirect("profile")
        profile = other_user.profile
        number_contacts = profile.following.all().count()
        questions = Question.objects.filter(respondent=other_user)
        answers = Answer.objects.all()
        context ={'profile': profile, 'other_user': other_user, "number_contacts": number_contacts, 
                    "questions": questions, "answers": answers, "form": form}
        return render(request, 'account/user_detail.html', context)

# Delete a profile
@login_required
def delete_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    user.delete()
    profile.delete()
    return redirect('index')

# Dipslay a list of all users
@login_required
def user_list(request):
    profiles = Profile.objects.exclude(user=request.user)  
    following= request.user.profile.following.all() 
    context = {'profiles': profiles, "following": following}
    return render(request, 'account/user_list.html', context)

# View search results
@login_required
def search_users(request):
    query = request.GET.get('q')
    user_list = User.objects.filter(username__icontains=query)
    profiles = Profile.objects.exclude(user=request.user)       
    context = {'users': user_list, 'profiles': profiles}
    return render(request, "account/search_users.html", context)

# Follow a user
@login_required
def follow(request, username):
    sender = request.user
    receiver = get_object_or_404(User, username=username)
    sender.profile.following.add(receiver.profile)
    create_action(request.user, 'follows', receiver)
    context = {'receiver': receiver}
    return render(request, "account/follow.html", context)

# Unfollow a user
@login_required
def unfollow(request, username):
    remover_profile = request.user.profile
    removee = get_object_or_404(User, username=username)
    removee_profile=removee.profile
    remover_profile.following.remove(removee_profile)
    create_action(request.user, 'unfollowed', removee)
    context ={ 'removee': removee}
    return render(request, "account/unfollow.html", context)

# Ask a question to a user
@login_required
def ask(request, username):
    if request.method == 'POST':    
        form = QuestionForm(request.POST)
        other_user = get_object_or_404(User, username=username)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.asker = request.user
            instance.respondent = other_user
            instance.save()
            create_action(instance.asker, ' asked a question ', instance.text)
        return redirect("user_detail", username=other_user.username)

# Delete a question
@login_required
def delete_question(request, pk):
    question = Question.objects.get(pk=pk)
    if question.respondent == request.user:
        question.delete()
        return redirect("profile")
    elif question.asker == request.user:
        question.delete()
        return redirect("user_detail", username = question.respondent.username)
    return redirect("profile")

# Answer a question
@login_required
def answer(request, pk):
    if request.method == 'POST': 
        question = Question.objects.get(pk=pk)   
        form = AnswerForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.question = question
            form.save()
            create_action(question.asker, 'answered a question', question.text)
        return redirect("profile")
    if request.method == 'GET':  
        form = AnswerForm()
        context = {"form": form}
        return render(request, 'account/profile.html', context)
    
# Delete an answer
@login_required
def delete_answer(request, pk):
    answer = Answer.objects.get(pk=pk)
    if answer.question.respondent == request.user:
        answer.delete()
    return redirect("profile")
