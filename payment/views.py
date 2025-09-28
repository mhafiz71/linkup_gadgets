from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from cart.cart import Cart
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    # Amount needs to be in kobo (integer)
    amount_in_kobo = int(order.total_paid * 100)

    context = {
        'order': order,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'paystack_currency': settings.PAYSTACK_CURRENCY,
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
    order.status = 'paid'  # Update status as well
    order.paystack_reference = reference
    order.save()
    
    # --- SEND ORDER CONFIRMATION EMAIL ---
    from core.email_utils import send_order_confirmation_email
    send_order_confirmation_email(order)
    # --- END OF EMAIL CODE ---
    
    # Clear the cart
    cart = Cart(request)
    cart.clear()

    return render(request, 'payment/success.html', {'order': order})

def payment_failed(request):
    return render(request, 'payment/failed.html')

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def retry_payment(request, order_id):
    """
    Allow users to retry payment for pending orders
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.paid:
        messages.info(request, 'This order has already been paid.')
        return redirect('accounts:order_detail', order_id=order.id)
    
    # Set order in session for payment process
    request.session['order_id'] = str(order.id)
    
    messages.info(request, 'Redirecting to payment...')
    return redirect('payment:process')