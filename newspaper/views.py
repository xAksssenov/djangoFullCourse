from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Article, Comment, Category
from .utils import find_matching_articles

def index(request):
    try:
        articles = Article.objects.all()
        categories = Category.objects.all()
        context = {'articles': articles, 'categories': categories}
    except Exception as e:
        print(f"Error in index view: {e}")
        raise Http404("Ошибка при получении данных")

    return render(request, "newspaper/index.html", context)

def detail(request, article_id):
    try:
        article = get_object_or_404(Article, pk=article_id)
        comments = Comment.objects.filter(article=article)
    except Http404:
        raise Http404("Статья не найдена")
    except Exception as e:
        print(f"Error in detail view: {e}")
        raise Http404("Ошибка при получении данных")

    context = {'article': article, 'comments': comments}
    return render(request, "newspaper/detail.html", context)

def polls(request):
    try:
        categories = Category.objects.all()
        context = {'categories': categories}
    except Exception as e:
        print(f"Error in polls view: {e}")
        raise Http404("Ошибка при получении данных")

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