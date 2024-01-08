from django.http import Http404
from django.shortcuts import render
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Category, Article, PurchaseLinks, Author, Tag
from .pagination import ArticlePagination, PurchaseLinksPagination
from .serializers import CategorySerializer, ArticleSerializer, PurchaseLinksSerializer
from .utils import filter_articles
from django.db.models import Sum
from django.db.models import Avg


def index(request):
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, "newspaper/list.html", context)


def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        links = PurchaseLinks.objects.filter(article=article)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, "newspaper/detail.html", {"article": article, 'links': links})


def polls(request):
    try:
        categories = Category.objects.all()
        tags = Tag.objects.all()
        authors = Author.objects.all()
        context = {'categories': categories, 'tags': tags, 'authors': authors}
    except:
        raise Http404("Error")
    return render(request, "newspaper/polls.html", context)


def find(request):
    selected_categories = request.POST.getlist('choiceCategories')
    selected_tags = request.POST.getlist('choiceTags')
    selected_authors = request.POST.getlist('choiceAuthors')

    articles = filter_articles(selected_categories, selected_tags, selected_authors)

    context = {
        'categories': selected_categories,
        'tags': selected_tags,
        'authors': selected_authors,
        'articles': articles
    }

    return render(request, "newspaper/findedArticles.html", context)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = ['category']


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = ArticlePagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ArticleFilter
    search_fields = ['name', 'category__name', 'tag__name']

    @action(detail=True, methods=['POST'])
    def add_purchase_link(self, request, pk=None):
        article = self.get_object()
        data = request.data
        data['article'] = article.id

        serializer = PurchaseLinksSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class PurchaseLinksViewSet(ModelViewSet):
    serializer_class = PurchaseLinksSerializer
    queryset = PurchaseLinks.objects.all()
    pagination_class = PurchaseLinksPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['website_name']


    @action(detail=False, methods=['GET'])
    def average_views_by_category(self, request):
        category_name = request.query_params.get('category', None)

        if category_name:
            articles = Article.objects.filter(category__name=category_name)
            views_by_article = PurchaseLinks.objects.filter(article__in=articles).values('article').annotate(average_views=Avg('readers_count'))

            result = [{'article': entry['article'], 'average_views': entry['average_views']} for entry in views_by_article]
            
            return Response(result)
        else:
            return Response({'error': 'Provide a category parameter'})

    @action(detail=False, methods=['GET'])
    def search_by_tag_and_author(self, request):
        tag_name = request.query_params.get('tag', None)
        author_name = request.query_params.get('author', None)

        if tag_name and author_name:
            articles = Article.objects.filter(tag__name=tag_name, author__name=author_name)
        elif tag_name:
            articles = Article.objects.filter(tag__name=tag_name)
        elif author_name:
            articles = Article.objects.filter(author__name=author_name)
        else:
            return Response({'error': 'Provide at least one of tag or author parameters'})

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
        
    @action(methods=['POST'], detail=True)
    def total_views(self, request, pk=None):
        articles = Article.objects.all()
        total_views = PurchaseLinks.objects.filter(article__in=articles).aggregate(Sum('readers_count'))['readers_count__sum']
        return Response({'total_views': total_views})


class FindArticlesViewSet(viewsets.ViewSet):
    serializer_class = ArticleSerializer

    def create(self, request):
        selected_categories = request.data.get('choiceCategories', [])
        selected_tags = request.data.get('choiceTags', [])
        selected_authors = request.data.get('choiceAuthors', [])

        articles = filter_articles(selected_categories, selected_tags, selected_authors)

        serializer = self.serializer_class(articles, many=True)

        response_data = {
            'categories': selected_categories,
            'tags': selected_tags,
            'authors': selected_authors,
            'articles': serializer.data
        }

        return Response(response_data)