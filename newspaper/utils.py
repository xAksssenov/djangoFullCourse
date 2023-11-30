from django.db.models import Q
from .models import Article

def find_matching_articles(selected_categories):
    query = Q()

    for category in selected_categories:
        query |= Q(section__name=category)

    matching_articles = Article.objects.filter(query).distinct()

    return matching_articles