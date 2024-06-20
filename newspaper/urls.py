from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ArticleViewSet,
    PurchaseLinksViewSet,
    FindArticlesViewSet,
    index,
    detail,
    polls,
    find,
)

app_name = 'newspaper'

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("articles", ArticleViewSet)
router.register("links", PurchaseLinksViewSet)
router.register('find-articles', FindArticlesViewSet, basename='find-articles')

urlpatterns = urlpatterns = [
    path('', index, name='index'),
    path('articles/<int:article_id>/', detail, name='detail'),
    path('polls/', polls, name='polls'),
    path('find/', find, name='find'),
] + router.urls