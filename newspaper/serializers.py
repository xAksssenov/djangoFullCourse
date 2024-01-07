from .models import Category, Article, PurchaseLinks, Author, Tag
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer(many=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'name', 'category', 'author', 'tag')


class PurchaseLinksSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = PurchaseLinks
        fields = '__all__'