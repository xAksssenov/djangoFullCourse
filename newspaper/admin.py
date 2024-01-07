from django.contrib import admin

from .models import Category, Article, PurchaseLinks, Author, Tag, ArticleAuthor, ArticleTag


class ArticleAuthorInline(admin.StackedInline):
    model = ArticleAuthor
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "get_authors", "get_tags"]
    filter_horizontal = ["author", "tag"]
    inlines = [ArticleAuthorInline]

    def get_authors(self, obj):
        return ", ".join([author.name for author in obj.author.all()])

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tag.all()])

    get_authors.short_description = "Авторы"
    get_tags.short_description = "Теги"


class PurchaseLinksAdmin(admin.ModelAdmin):
    list_display = ["website_name", "url", "display_article_name", "readers_count", "popular"]
    list_display_links = ["website_name", "url"]
    list_filter = ["article"]
    search_fields = ["website_name"]
    fieldsets = [
        ("Название сайта", {"fields": ["website_name"]}),
        ("Остальная информация", {"fields": ["url", "article", "readers_count"]}),
    ]

    def display_article_name(self, obj):
        return obj.article.name

    display_article_name.short_description = "Статья"


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ['display_tag', 'display_article']
    list_display_links = ['display_tag', 'display_article']
    filter_horizontal = ['article', 'tag']
    list_filter = ['article', 'tag']

    def display_tag(self, obj):
        return ", ".join([tag.name for tag in obj.tag.all()])

    def display_article(self, obj):
        return ", ".join([article.name for article in obj.article.all()])

    display_tag.short_description = "Теги"
    display_article.short_description = "Статьи"

    
class ArticleAuthorAdmin(admin.ModelAdmin):
    list_display = ['author', 'article']
    list_filter = ['author']
    search_fields = ["article"]
    raw_id_fields = ['article']


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(PurchaseLinks, PurchaseLinksAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(ArticleAuthor, ArticleAuthorAdmin)