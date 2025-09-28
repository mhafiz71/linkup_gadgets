from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart

@require_POST
def add_to_cart(request, product_id):
    from django.contrib import messages
    
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if product is in stock
    if product.stock_quantity <= 0:
        messages.error(request, f'Sorry, "{product.name}" is currently out of stock.')
        return redirect('shop:product_detail', slug=product.slug)
    
    # Check if requested quantity exceeds available stock
    current_cart_quantity = cart.get_item_quantity(product.id)
    total_requested = current_cart_quantity + quantity
    
    if total_requested > product.stock_quantity:
        available = product.stock_quantity - current_cart_quantity
        if available > 0:
            messages.warning(request, f'Only {available} more units of "{product.name}" can be added to your cart.')
        else:
            messages.error(request, f'You already have the maximum available quantity of "{product.name}" in your cart.')
        return redirect('shop:product_detail', slug=product.slug)

    cart.add(product=product, quantity=quantity, override_quantity=False)
    messages.success(request, f'"{product.name}" has been added to your cart.')
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
            messages.success(request, f'Cart updated successfully.')
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity specified.')
        
    return redirect('cart:cart_detail')