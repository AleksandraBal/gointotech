from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from actions.utils import create_action

# Display all threads
@login_required
def thread_list(request):
    thread_list = Thread.objects.all()
     # Pagination with 10 threads per page
    paginator = Paginator(thread_list, 10)
    page_number = request.GET.get('page')
    try:
        threads = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        threads = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        threads = paginator.page(paginator.num_pages)
    context= {'threads': threads}
    return render(request, 'forum/thread_list.html', context)

# Create a new thread
@login_required
def add_thread(request):
    user = request.user
    if request.method == "GET":
        thread_form = ThreadForm()
        post_form = PostForm()
        context = {'thread_form': thread_form, 'post_form': post_form}
        return render(request, 'forum/add_thread.html', context)
    if request.method == "POST":
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        if thread_form.is_valid():
            data = thread_form.save(commit=False)
            data.author = user
            data.save()
            create_action(request.user, 'created a new forum thread', data)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = user
            post.thread = data
            post.save()
            create_action(request.user, 'created a new forum thread', post)
        return redirect('forum:thread_list')

# Delete a thread
@login_required
def delete_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.user == thread.author:
        create_action(request.user, 'deleted a forum thread', thread)
        thread.delete()
    return redirect('forum:thread_list')

# View all posts belonging to a thread
@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.posts.all()
    if request.method == "GET":   
        form = PostForm()
        return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts, 'form': form})
    if request.method == "POST":
        form = PostForm(request.POST)       
        if form.is_valid():
            # Create a Post object without saving it to the database
            instance = form.save(commit=False)
            # Assign the thread and the author to the comment
            instance.author = request.user
            instance.thread = thread
            # Save the post to the database
            instance.save()
            create_action(request.user, 'posted on the forum', instance)
        return redirect('forum:thread_detail', thread.pk)

# Delete a post
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    thread = post.thread
    if request.user == post.author:
        create_action(request.user, 'deleted a forum post', post)
        post.delete()
    elif request.user == thread.author:
        create_action(request.user, 'deleted a forum post', post)
        post.delete()
    return redirect('forum:thread_detail', pk=thread.pk)

# Edit a post
@login_required
def edit_post(request, pk):
    edited_post = get_object_or_404(Post, pk=pk)
    thread = edited_post.thread
    posts = thread.posts.all()
    if request.method == 'GET':
        form = PostForm(instance=edited_post)
        return render(request, "forum/edit_post.html", {"form": form, "thread": thread, "posts": posts, "edited_post": edited_post})
    if request.method == 'POST':	
	    form = PostForm(instance=edited_post, data=request.POST)
	    if form.is_valid():
		    form.save()
	    return redirect('forum:thread_detail', pk=thread.pk)

# Add or remove a "like"   
@login_required
def like(request, pk):
    post = get_object_or_404(Post, id=pk)
    thread = post.thread
    already_liked = PostLike.objects.filter(user=request.user, post=post).count()
    if already_liked > 0 and post.author != request.user:
        like = PostLike.objects.filter(user=request.user, post=post)[0]
        like.delete()
    elif post.author != request.user:
        PostLike.objects.create(user=request.user, post=post)
        create_action(request.user, 'liked', post)
    return redirect('forum:thread_detail', pk=thread.pk)

