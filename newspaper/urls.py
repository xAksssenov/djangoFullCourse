from django.urls import path
from . import views

app_name = 'newspaper'

urlpatterns = [
    path('', views.list, name='list'),
    path('article/<int:article_id>/', views.detail, name='detail'),
    path('polls', views.polls, name='polls'),
    path('find', views.find, name='find'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
]