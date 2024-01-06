from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'articles'

router = DefaultRouter()
router.register("articles", views.ArticlesViewSet)
router.register("my-articles", views.CurrentUserArticlesViewSet)
router.register("comments", views.CommentsViewSet)

urlpatterns = [] + router.urls