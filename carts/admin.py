from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']  # Removed 'created_at'
    inlines = [CartItemInline]
    search_fields = ['cart_id']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'is_active']
    list_filter = ['is_active', 'cart']
    search_fields = ['product__product_name', 'cart__cart_id']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
