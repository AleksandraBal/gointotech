from django.shortcuts import render
from ..models import *
from django.http import JsonResponse 
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status 
from rest_framework.views import APIView 
from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .permissions import *

class ArticleCreate(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Article.objects.all()

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

class ArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsArticleAuthorOrReadOnly]
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Article.objects.filter(pk=pk)
    
class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comment.objects.filter(article=pk)
    
class CommentAdd(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        article = Article.objects.get(pk=pk)
        author = self.request.user
        serializer.save(article=article, author=author)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrReadOnly]
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comment.objects.filter(pk=pk)
    
class Like(generics.RetrieveAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        article = Article.objects.get(pk=pk)
        user = self.request.user
        serializer.save(article=article, user=user)