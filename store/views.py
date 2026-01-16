from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

# Store view — all products
def store(request):
    products = Product.objects.filter(is_available=True)
    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


# Products by category
def products_by_category(request, category_slug=None):
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)
    
    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


# Product detail view — added to fix the error
def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    context = {
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # cart logic will be added later
    return redirect('store')