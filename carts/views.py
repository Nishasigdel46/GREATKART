from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.shortcuts import render

# Get or create cart
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# Add to cart / Increase quantity
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except:
                pass

    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    if cart_items.exists():
        # ✅ loop properly indented inside if
        for item in cart_items:
            if set(item.variations.all()) == set(product_variation):
                # enforce max quantity 10
                if item.quantity < 10:
                    item.quantity += 1
                    item.save()
                return redirect('cart')

        # No matching variation → create new CartItem
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.variations.add(*product_variation)

    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.variations.add(*product_variation)

    return redirect('cart')


# Decrease quantity
def remove_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove item if quantity reaches 0
    return redirect('cart')

# Remove entire item (regardless of quantity)
def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

# Cart page
def cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)

        total = sum(item.product.price * item.quantity for item in cart_items)
        quantity = sum(item.quantity for item in cart_items)
        tax = (2 * total) / 100
        grand_total = total + tax
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


# carts/views.py
def signin(request):
    return render(request, 'signin.html')  # make sure template exists in templates/
