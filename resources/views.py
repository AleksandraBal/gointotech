from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from actions.utils import create_action

# Display all articles
def article_list(request):
    article_list= Article.objects.all()
    # Pagination with 3 posts per page
    paginator = Paginator(article_list, 3)
    page_number = request.GET.get('page')
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    return render(request, 'resources/article_list.html', {'articles': articles})

# Display one  article
def article_detail(request, year, month, day, article):
    article = get_object_or_404(Article, slug=article,
                             created__year=year,
                             created__month=month,
                             created__day=day)
    # List of active comments for this post
    comments = article.comments.all()
    # Form for users to comment
    form = CommentForm()
    return render(request, 'resources/article.html', {'article': article, 'comments': comments, 'form': form})

# Add a comment to an article
@require_POST
def article_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    slug = article.slug
    year = article.created.year
    month = article.created.month
    day = article.created.day
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post and the author to the comment
        comment.article = article
        comment.author = request.user
        # Save the comment to the database
        comment.save()
        create_action(request.user, 'commented', comment)
    return redirect('resources:article_detail', article=slug, day=day, month=month, year=year)

# Delete an article
@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user == article.author:
        create_action(request.user, 'deleted article', article)
        article.delete()
    return redirect('resources:article_list')

# Edit an article
@login_required
def edit_article(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        form = ArticleForm(instance=article, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            create_action(request.user, 'edited article', article)
        return redirect('resources:article_list')
    if request.method == 'GET':
        article = get_object_or_404(Article, id=article_id)
        form = ArticleForm(instance=article)
        return render(request, "resources/edit_article.html", {"form": form})

# Delete an article
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    article = comment.article
    slug = article.slug
    year = article.created.year
    month = article.created.month
    day = article.created.day
    if request.user== comment.author:
        create_action(request.user, 'deleted comment', article)
        comment.delete()
    return redirect('resources:article_detail', article=slug, day=day, month=month, year=year)

# Write a new article
@login_required
def add_article(request):
    user = request.user
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.author = user
            data.save()
            create_action(request.user, 'wrote article', data)
        return redirect('resources:article_list')
    else:
        form = ArticleForm()
        return render(request, 'resources/add_article.html', {'form': form})

# Add or remove a "like"
@login_required
def like(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    slug = article.slug
    year = article.created.year
    month = article.created.month
    day = article.created.day
    already_liked = Like.objects.filter(user=request.user, article=article).count()
    if already_liked > 0 and article.author != request.user:
        like = Like.objects.filter(user=request.user, article=article)[0]
        like.delete()
    elif article.author != request.user:
        Like.objects.create(user=request.user, article=article)
        create_action(request.user, 'liked article', article)
    return redirect('resources:article_detail', article=slug, day=day, month=month, year=year)