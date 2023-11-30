from django.db.models import Q
from .models import Article

def find_matching_articles(selected_categories):
    query = Q()

    for categories in selected_categories:
        query |= Q(categories__name=categories)

    matching_articles = Article.objects.filter(query).distinct()

    return matching_articles