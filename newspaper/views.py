import datetime

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Article, Author, Comment, Category
from .utils import find_matching_articles
from .forms import ArticleForm
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet
from .models import Category, Author, Article
from .serializers import CategorySerializer, AuthorSerializer, ArticleSerializer
from .pagination import ArticlePagination

def list(request):

    articles = Article.objects.all()
    categories = Category.objects.all()
    context = {'articles': articles, 'categories': categories}
   
    return render(request, "newspaper/list.html", context)

def detail(request, article_id):

    article = get_object_or_404(Article, pk=article_id)
    comments = Comment.objects.filter(article=article)
    context = {'article': article, 'comments': comments}

    return render(request, "newspaper/detail.html", context)

def polls(request):

    categories = Category.objects.all()
    context = {'categories': categories}

    return render(request, "newspaper/polls.html", context)

def find(request):

    selected_categories = request.GET.getlist('choiceCategories')
    matching_articles = find_matching_articles(selected_categories)
    
    context = {
        'selected_categories': selected_categories,
        'articles': matching_articles  
    }
    
    return render(request, "newspaper/find.html", context)

def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            Author.name = request.user
            article.publication_date = timezone.now()
            article.save()
            return redirect('newspaper:detail', article_id=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'newspaper/article_edit.html', {'form': form})

def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            Author.name = request.user
            article.published_date = timezone.now()
            article.save()
            return redirect('newspaper:detail', article_id=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'newspaper/article_edit.html', {'form': form})

class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    queryset = Article.objects.all()
    
class CurrentUserArticlesViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(Q(author=user) | (Q(author__username='specific_author') & Q(
            pub_date__gte=timezone.now() - datetime.timedelta(days=7))))