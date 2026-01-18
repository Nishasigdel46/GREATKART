from django.contrib import admin
from .models import Product, Variation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'price',
        'stock',
        'category',
        'created_date',
        'is_available',
    )
    list_filter = ('is_available', 'category')
    search_fields = ('product_name',)
    prepopulated_fields = {'slug': ('product_name',)}


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'variation_category',
        'variation_value',
        'is_active',
        'created_date',
    )
    list_editable = ('is_active',)
    list_filter = ('variation_category', 'is_active')
    search_fields = ('product', 'variation_category','variation_value')
