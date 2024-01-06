import datetime

from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords
from django.utils import timezone


class Article(models.Model):
    article_title = models.CharField('Название статьи', max_length=200)
    article_text = models.TextField('Текст статьи')
    pub_date = models.DateTimeField('Дата публикации', default=datetime.datetime.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name='Автор')

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=7))

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name = models.CharField(verbose_name='Имя автора', max_length=50, default='Имя')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    comment_text = models.CharField(verbose_name='Текст комментария', max_length=200)
    image = models.ImageField(verbose_name='Изображение', upload_to='comment_images/', blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'