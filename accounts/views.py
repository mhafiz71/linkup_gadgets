from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from orders.models import Order, OrderItem
from django.db import transaction
from .forms import UserRegisterForm, VendorRegisterForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def order_detail(request, order_id):
    try:
        # Ensure the order belongs to the logged-in user to prevent unauthorized access
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        raise Http404("Order not found")
        
    return render(request, 'accounts/order_detail.html', {'order': order})

@transaction.atomic
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        vendor_form = VendorRegisterForm(request.POST, request.FILES)
        
        # Check if the user wants to register as a vendor
        is_vendor = 'is_vendor' in request.POST

        if user_form.is_valid() and (not is_vendor or vendor_form.is_valid()):
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            if is_vendor:
                vendor = vendor_form.save(commit=False)
                vendor.user = user
                vendor.save()
                messages.success(request, f'Vendor account created for {user.username}! You can now log in.')
            else:
                messages.success(request, f'Customer account created for {user.username}! You can now log in.')
            
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegisterForm()
        vendor_form = VendorRegisterForm()

    context = {
        'user_form': user_form,
        'vendor_form': vendor_form
    }
    return render(request, 'accounts/register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('index')

            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')


@login_required
def customer_profile(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def delete_order(request, order_id):
    """
    Handles the deletion of a user's order with a confirmation step.
    """
    # Ensure the order exists and belongs to the logged-in user for security
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # We'll only allow deleting orders that have not been marked as paid
    if order.paid:
        messages.error(request, 'Cannot cancel an order that has already been paid.')
        return redirect('accounts:order_detail', order_id=order.id)

    if request.method == 'POST':
        # If the form is submitted, it's a confirmation.
        order_id_copy = str(order.id) # Copy the ID before it's deleted
        order.delete()
        messages.success(request, f"Order #{order_id_copy[:8]} has been successfully cancelled.")
        return redirect('accounts:profile') # Redirect to the order history page
    
    # If it's a GET request, show the confirmation page.
    return render(request, 'accounts/delete_order_confirm.html', {'order': order})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Pass instance=request.user to pre-fill the form and save to the correct user
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        # On a GET request, show the form pre-filled with the user's current data
        form = UserEditForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})


