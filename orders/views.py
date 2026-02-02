import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from carts.models import CartItem
from .models import Order, Payment, OrderProduct
from .forms import OrderForm
from django.http import HttpResponse

def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')  # Redirect if cart is empty

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity
    tax = (2 * total) / 100  # Example: 2% tax
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
        #Store all the billing informations inside Order table 
            order = Order()
            order.user = current_user
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address_line_1 = form.cleaned_data['address_line_1']
            order.address_line_2 = form.cleaned_data['address_line_2']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.order_note = form.cleaned_data.get('order_note', '')  
            order.order_total = grand_total
            order.tax = tax
            order.save()

            # Generate order number
            today_date = datetime.date.today().strftime('%Y%m%d')
            order_number = today_date + str(order.id)
            order.order_number = order_number
            order.save()

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')  # Redirect if not POST

def review_order(request, order_number):
    current_user = request.user

    # Get the order by order_number
    order = get_object_or_404(Order, order_number=order_number, user=current_user)

    # Get cart items for that user
    cart_items = CartItem.objects.filter(user=current_user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    context = {
        'order': order,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'orders/review_order.html', context)

from django.shortcuts import get_object_or_404, redirect
from .models import Order, Payment

def payments(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        # Get the latest unpaid order for this user
        order = Order.objects.filter(user=request.user, is_ordered=False).order_by('-created_at').first()

        if not order:
            # No unpaid orders found
            messages.error(request, "No pending order found to process payment.")
            return redirect('cart')  # Or wherever you want

        payment = Payment(
            user=request.user,
            payment_id=f"{order.order_number}_{payment_method}",
            payment_method=payment_method,
            amount_paid=order.order_total,
            status='Completed' if payment_method=='cod' else 'Pending',
        )
        payment.save()

        order.is_ordered = True
        order.payment = payment
        order.save()

        return redirect('order_complete', order_number=order.order_number)


def order_complete(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order
    }
    return render(request, 'orders/order_complete.html', context)
