# Generated by Django 4.2.7 on 2024-01-07 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newspaper', '0004_historicalcategory_historicalarticle'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Автор статьи',
                'verbose_name_plural': 'Авторы статьи',
            },
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Тег статьи',
                'verbose_name_plural': 'Теги статьи',
            },
        ),
        migrations.CreateModel(
            name='HistoricalAuthor',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Автор')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Автор',
                'verbose_name_plural': 'historical Авторы',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='PurchaseLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('readers_count', models.IntegerField(verbose_name='Количество читателей')),
            ],
            options={
                'verbose_name': 'Ссылка на статью',
                'verbose_name_plural': 'Ссылки на статью',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.RemoveField(
            model_name='comment',
            name='article',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='reader',
        ),
        migrations.RemoveField(
            model_name='historicalarticle',
            name='author',
        ),
        migrations.RemoveField(
            model_name='historicalarticle',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalarticle',
            name='section',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='historicalcategory',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Категория', 'verbose_name_plural': 'historical Категории'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='content',
        ),
        migrations.RemoveField(
            model_name='article',
            name='publication_date',
        ),
        migrations.RemoveField(
            model_name='article',
            name='section',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title',
        ),
        migrations.RemoveField(
            model_name='author',
            name='email',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='newspaper.category', verbose_name='Категория'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Заголовок статьи'),
        ),
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='historicalcategory',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название категории'),
        ),
        migrations.DeleteModel(
            name='Advertiser',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='HistoricalArticle',
        ),
        migrations.DeleteModel(
            name='Reader',
        ),
        migrations.AddField(
            model_name='purchaselinks',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newspaper.article'),
        ),
        migrations.AddField(
            model_name='articletag',
            name='article',
            field=models.ManyToManyField(to='newspaper.article'),
        ),
        migrations.AddField(
            model_name='articletag',
            name='tag',
            field=models.ManyToManyField(to='newspaper.tag'),
        ),
        migrations.AddField(
            model_name='articleauthor',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newspaper.article'),
        ),
        migrations.AddField(
            model_name='articleauthor',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newspaper.author'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(to='newspaper.tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ManyToManyField(to='newspaper.author'),
        ),
    ]