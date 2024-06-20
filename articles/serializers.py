from .models import Article, Comment
from django.contrib.auth import get_user_model
from rest_framework import serializers

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'article',
            'author',
            'comment_text',
        ]

    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        user = obj.author
        return user.username

    def validate_comment_text(self, value):
        if len(value) > 200:
            raise serializers.ValidationError("Длина комментария не должна превышать 200 символов.")
        return value

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'article_title', 'article_text', 'pub_date']

    def validate_article_title(self, value):
        if not value[0].isupper():
            raise serializers.ValidationError("Заголовок статьи должен начинаться с большой буквы.")
        return value