import datetime

from django.contrib import admin
from django.utils import timezone
from import_export import resources
from import_export.admin import ExportActionMixin

from .models import Article, Comment

class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article

    def get_export_queryset(self, request):
        qs = super().get_export_queryset(request)
        return qs.filter(pub_date__gte=timezone.now() - datetime.timedelta(days=30))

    def dehydrate_pub_date(self, article):
        return article.pub_date.strftime("%Y-%m-%d %H:%M")
    
class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment

    def get_author_name(self, comment):
        return comment.author.username

class ArticleAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ArticleResource
    list_display = ['article_title', 'author', 'pub_date']
    date_hierarchy = 'pub_date'
    readonly_fields = ['pub_date']

class CommentAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = CommentResource
    list_display = ['article', 'author_name', 'author', 'image']
    list_filter = ['article']
    search_fields = ["author_name"]
    fieldsets = [
        ("Статья", {"fields": ["article"]}),
        ("Пользователь", {"fields": ["author_name", 'author', 'comment_text', 'image']}),
    ]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)