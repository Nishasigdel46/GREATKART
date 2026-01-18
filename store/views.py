from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from django.db.models import Q

from carts.views import _cart_id
from django.core.paginator import Paginator
from django.http import HttpResponse

# Store view — all products
def store(request):
    products = Product.objects.filter(is_available=True).order_by('id')
    paginator = Paginator(products, 3)  
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
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
    single_product = get_object_or_404(
        Product,
        slug=product_slug,
        category__slug=category_slug
    )

    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request),
        product=single_product
    ).exists()

    sizes = single_product.variations.filter(
        variation_category='size',
        is_active=True
    )

    colors = single_product.variations.filter(
        variation_category='color',
        is_active=True
    )

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'sizes': sizes,
        'colors': colors,
    }

    return render(request, 'store/product_detail.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # cart logic will be added later
    return redirect('cart')


def search(request):
    keyword = request.GET.get('keyword')  # safely get keyword
    if keyword:
        products = Product.objects.filter(
            Q(product_name__icontains=keyword) | Q(description__icontains=keyword)
        ).order_by('-created_date')
    else:
        products = Product.objects.none()  # show 0 products if nothing typed

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

