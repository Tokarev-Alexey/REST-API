from posts.models import Post, Comment
from rest_framework import serializers

from users.models import ProfileUser


class CommentSerializer(serializers.ModelSerializer):
    author_comm = serializers.ReadOnlyField(source='author_comm.username')

    class Meta:
        model = Comment
        fields = ['id', 'author_comm', 'text_comm', 'pub_date', 'post']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'text', 'pub_date', 'comments']


