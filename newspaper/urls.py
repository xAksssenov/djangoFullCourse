from rest_framework.routers import DefaultRouter
from . import views

app_name = 'newspaper'

router = DefaultRouter()
router.register("articles", views.ArticleViewSet)
router.register("my-articles", views.CurrentUserArticlesViewSet)

urlpatterns = [] + router.urls
