from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Раздел газеты'
        verbose_name_plural = 'Разделы газеты'

class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Article(models.Model):
    title = models.CharField(max_length=255)
    section = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Advertiser(models.Model):
    name = models.CharField(max_length=255)
    ads_published = models.ManyToManyField(Article)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рекламодатель'
        verbose_name_plural = 'Рекламодатели'

class Reader(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.reader} к {self.article}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'