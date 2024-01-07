from django.db.models import Q

from .models import Article


def filter_articles(categories, tags, authors):
    """
    Функция для фильтрации статей по категориям, тегам и авторам.

    :param categories: Список категорий
    :param tags: Список тегов
    :param authors: Список авторов
    :return: QuerySet статей
    """
    # Используем Q-объекты для построения сложных запросов
    category_q = Q(category__name__in=categories) if categories else Q()
    tag_q = Q(tag__name__in=tags) if tags else Q()
    author_q = Q(author__name__in=authors) if authors else Q()

    # Выполняем запрос к базе данных
    articles = Article.objects.filter(category_q & tag_q & author_q)

    return articles