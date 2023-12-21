from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import CategoryViewSet, AuthorViewSet, ArticleViewSet

app_name = 'newspaper'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('', views.list, name='list'),
    path('article/<int:article_id>/', views.detail, name='detail'),
    path('polls', views.polls, name='polls'),
    path('find', views.find, name='find'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
]

urlpatterns.extend(router.urls)