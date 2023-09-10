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

@login_required
def mailbox(request):
    threads = MailThread.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    names_to_exclude = [request.user.username, "admin"] 
    users=User.objects.exclude(username__in=names_to_exclude)
    context = {'threads': threads, "users": users}
    return render(request, 'mail/mailbox.html', context)

@login_required
def thread(request, username):
    if request.method == 'GET':
        form = MessageForm()
        user = User.objects.get(username=username)
        if MailThread.objects.filter(sender=request.user, receiver=user).exists():
            thread = MailThread.objects.filter(sender=request.user, receiver=user)[0]
        elif MailThread.objects.filter(receiver=request.user, sender=user).exists():
            thread = MailThread.objects.filter(receiver=request.user, sender=user)[0]
        else:
            thread = MailThread(sender=request.user, receiver=user)
            thread.save()
        message_list = Message.objects.filter(thread=thread.pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }
        return render(request, 'mail/thread.html', context)

@login_required
def new_message(request, pk):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        thread = get_object_or_404(MailThread, pk=pk)
        if thread.receiver == request.user:
            receiver = thread.sender
        else:
            receiver = thread.receiver
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender_user = request.user
            instance.receiver_user = receiver
            instance.thread = thread
            instance.save()
        return redirect('thread', username=receiver.username)

@login_required
def delete_thread(request, pk):
    thread = get_object_or_404(MailThread, pk=pk)
    thread.delete()
    return redirect("mailbox")

@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.delete()
    if message.receiver_user == request.user:
        return redirect("thread", message.sender_user.username)
    elif message.sender_user == request.user:
        return redirect("thread", message.receiver_user.username)