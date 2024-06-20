# Generated by Django 4.2.6 on 2024-06-19 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VisitLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=10)),
                ('get_params', models.TextField()),
                ('post_params', models.TextField()),
                ('user_agent', models.CharField(max_length=255)),
                ('ip_address', models.GenericIPAddressField()),
            ],
        ),
    ]