from django.contrib import admin
from .models import Category, Article, Author, Advertiser, Reader, Comment

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "section", "publication_date"]
    fieldsets = [
        (None, {"fields": ["title", "section", "content"]}),
    ]
    inlines = [CommentInline]

class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ["name"]
    filter_horizontal = ['ads_published']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'reader', 'text', 'timestamp']
    list_filter = ['article', 'reader']

admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(Reader)
admin.site.register(Comment, CommentAdmin)