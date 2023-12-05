# Generated by Django 4.2.7 on 2023-12-05 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newspaper', '0002_remove_advertiser_ads_published_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertiser',
            name='published_ads',
        ),
        migrations.RemoveField(
            model_name='article',
            name='advertisers',
        ),
        migrations.AddField(
            model_name='advertiser',
            name='ads_published',
            field=models.ManyToManyField(to='newspaper.article'),
        ),
    ]