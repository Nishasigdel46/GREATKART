from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'price',
        'stock',
        'category',        # ✅ comma added
        'created_date',
        'is_available',
    )
    list_filter = ('is_available',)
    search_fields = ('product_name',)
    prepopulated_fields = {'slug': ('product_name',)}
