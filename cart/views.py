from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart

@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Simple stock check
    if quantity > product.stock_quantity:
        # Handle this properly with a message in a real app
        return redirect('shop:product_detail', slug=product.slug)

    cart.add(product=product, quantity=quantity, override_quantity=False)
    return redirect('cart:cart_detail')

@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def update_cart(request, product_id):
    """
    Updates the quantity of a product in the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity'))
        if quantity <= 0:
            # If quantity is 0 or less, remove the item
            cart.remove(product)
            messages.info(request, f'"{product.name}" was removed from your cart.')
        elif quantity > product.stock_quantity:
            messages.error(request, f'Sorry, only {product.stock_quantity} units of "{product.name}" are available.')
        else:
            # Use the 'add' method with override_quantity=True to set the new quantity
            cart.add(product=product, quantity=quantity, override_quantity=True)
            messages.success(request, f'Your cart has been updated.')
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity specified.')
        
    return redirect('cart:cart_detail')