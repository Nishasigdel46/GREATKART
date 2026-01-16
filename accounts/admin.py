from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'date_joined',
        'last_login',
        'is_active',
        'is_admin',
    )

    list_filter = ('is_active', 'is_admin')
    search_fields = ('email', 'username')
    ordering = ('email',)
