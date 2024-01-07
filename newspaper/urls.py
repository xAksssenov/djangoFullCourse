from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ArticleViewSet,
    PurchaseLinksViewSet,
    FindArticlesViewSet
)

app_name = 'newspaper'

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("articles", ArticleViewSet)
router.register("links", PurchaseLinksViewSet)
router.register('find-articles', FindArticlesViewSet, basename='find-articles')

urlpatterns = [] + router.urls