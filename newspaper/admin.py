from django.contrib import admin

from .models import Category, Article, Author, Advertiser, Reader, Comment

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "section", "author","short_content", "publication_date"]
    list_filter = ["section"]
    date_hierarchy = "publication_date"
    list_display_links = ["title", "section", "author"]
    search_fields = ["title"]
    
    @admin.display(description='Short Content')
    def short_content(self, obj):
        return f"{obj.content[:50]}..." if len(obj.content) > 50 else obj.content

    inlines = [CommentInline]
    raw_id_fields = ["author"]

    fieldsets = [
        (None, {"fields": ["title", "section", "content", "author"]}),
    ]

class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ["name"]
    filter_horizontal = ['ads_published']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'reader', 'text', 'timestamp']
    list_filter = ['article', 'reader']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "email"]
    search_fields = ["name", "email"]
    list_filter = ["name"]

class ReaderAdmin(admin.ModelAdmin):
    list_display = ["name", "email"]
    search_fields = ["name", "email"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]

admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(Reader)
admin.site.register(Comment, CommentAdmin)