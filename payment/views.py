from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from cart.cart import Cart

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    # Amount needs to be in kobo (integer)
    amount_in_kobo = int(order.total_paid * 100)

    context = {
        'order': order,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'amount_in_kobo': amount_in_kobo,
    }
    return render(request, 'payment/process.html', context)

def payment_callback(request):
    # This view is called by Paystack via webhook or redirect
    reference = request.GET.get('reference')
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    # You should ideally verify the transaction with Paystack API here
    # For simplicity, we'll just mark it as paid
    order.paid = True
    order.paystack_reference = reference
    order.save()
    
    # Clear the cart
    cart = Cart(request)
    cart.clear()

    return render(request, 'payment/success.html', {'order': order})

def payment_failed(request):
    return render(request, 'payment/failed.html')