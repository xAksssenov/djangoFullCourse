from django.urls import path
from . import views

app_name = 'newspaper'

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:article_id>/', views.detail, name='detail'),
    path('polls', views.polls, name='polls'),
    path('find', views.find, name='find'),
]