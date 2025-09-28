from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from orders.models import Order
from cart.cart import Cart

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    amount_in_kobo = int(order.total_paid * 100)

    context = {
        'order': order,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'paystack_currency': settings.PAYSTACK_CURRENCY,
        'amount_in_kobo': amount_in_kobo,
    }
    return render(request, 'payment/process.html', context)

def payment_callback(request):
    reference = request.GET.get('reference')
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    order.paid = True
    order.status = 'paid'
    order.paystack_reference = reference
    order.save()
    
    from core.email_utils import send_order_confirmation_email
    send_order_confirmation_email(order)
    
    cart = Cart(request)
    cart.clear()

    return render(request, 'payment/success.html', {'order': order})

def payment_failed(request):
    return render(request, 'payment/failed.html')

@login_required
def retry_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.paid:
        messages.info(request, 'This order has already been paid.')
        return redirect('accounts:order_detail', order_id=order.id)
    
    request.session['order_id'] = str(order.id)
    messages.info(request, 'Redirecting to payment...')
    return redirect('payment:process')