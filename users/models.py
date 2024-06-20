from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from simple_history.models import HistoricalRecords

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    history = HistoricalRecords()
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
