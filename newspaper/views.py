from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Article, Comment, Category
from .utils import find_matching_articles

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
    
        selected_sections = request.GET.getlist('section')
        selected_authors = request.GET.getlist('author')
        publication_date = request.GET.get('publication_date', None)

        news = find_matching_articles(selected_sections, selected_authors, publication_date)

        context = {
        'brands': selected_sections,
        'styles': selected_authors,
        'colors': publication_date,
        'models': news
        }

        return render(request, "newspaper/find_articles.html", context)