from rest_framework import serializers
from ..models import *

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ('slug', 'image', "author")

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('author', 'article')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
    