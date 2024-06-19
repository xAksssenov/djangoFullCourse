from django.contrib import admin

from users.models import User
from products.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    inlines = (BasketAdmin,)
    search_fields = ('username',)
    ordering = ('-username',)
    readonly_fields = ('is_staff',)
