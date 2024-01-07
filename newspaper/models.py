from django.contrib import admin
from django.db import models
from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Автор')
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='Заголовок статьи', default="")
    author = models.ManyToManyField(Author)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class ArticleAuthor(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Автор статьи'
        verbose_name_plural = 'Авторы статьи'

    def __str__(self):
        return f"{self.article} - {self.author}"


class ArticleTag(models.Model):
    article = models.ManyToManyField(Article)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{', '.join(str(name) for name in self.tag.all())} - {', '.join(str(article) for article in self.article.all())}"

    class Meta:
        verbose_name = 'Тег статьи'
        verbose_name_plural = 'Теги статьи'


class PurchaseLinks(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    website_name = models.CharField(max_length=255)
    url = models.URLField()
    readers_count = models.IntegerField(verbose_name='Количество читателей')

    def __str__(self):
        return self.website_name

    @admin.display(
        boolean=True,
        ordering="readers_count",
        description="Популярная статья?",
    )
    def popular(self):
        return self.readers_count > 10000

    class Meta:
        verbose_name = 'Ссылка на статью'
        verbose_name_plural = 'Ссылки на статью'