from django.db.models import Q
from .models import Article

def find_matching_articles(selected_sections, selected_authors, publication_date):
    query = Q()

    for section in selected_sections:
        query |= Q(section__name=section)

    for author in selected_authors:
        query &= Q(author__name=author)

    if publication_date:
        query &= Q(publication_date=publication_date)

    matching_articles = Article.objects.filter(query).distinct()

    return matching_articles