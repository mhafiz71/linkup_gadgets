from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction
from django.http import Http404

# --- Email Imports ---
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# --- Local Imports ---
from .forms import UserRegisterForm, VendorRegisterForm, UserEditForm
from orders.models import Order


@transaction.atomic
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)

        # Check which button was pressed
        if 'submit_vendor' in request.POST:
            vendor_form = VendorRegisterForm(request.POST, request.FILES)
            
            if user_form.is_valid() and vendor_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                vendor = vendor_form.save(commit=False)
                vendor.user = user
                vendor.save()

                # Send email, show success, redirect
                messages.success(request, f'Vendor account created for {user.username}! You can now log in.')
                # (You should add the email sending code here too)
                return redirect('accounts:login')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif 'submit_customer' in request.POST:
            vendor_form = VendorRegisterForm() # Create an empty form
            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                # Send email, show success, redirect
                messages.success(request, f'Customer account created for {user.username}! You can now log in.')
                # (You should add the email sending code here too)
                return redirect('accounts:login')
            else:
                messages.error(request, 'Please correct the errors in your personal details.')
        
        else: # Should not happen, but good practice
            vendor_form = VendorRegisterForm()
            messages.error(request, 'An unexpected error occurred. Please try again.')

    else: # GET request
        user_form = UserRegisterForm()
        vendor_form = VendorRegisterForm()

    context = {
        'user_form': user_form,
        'vendor_form': vendor_form
    }
    return render(request, 'accounts/register.html', context)

def login_view(request):
    """
    Handles user login. Redirects to the 'next' page if provided.
    """
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
    """
    Handles user logout.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')


@login_required
def customer_profile(request):
    """
    Displays the customer's profile page with their order history.
    """
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """
    Handles the form for users to edit their personal information.
    """
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def order_detail(request, order_id):
    """
    Displays the details of a single order, ensuring the order
    belongs to the logged-in user.
    """
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        raise Http404("Order not found")
        
    return render(request, 'accounts/order_detail.html', {'order': order})


@login_required
def delete_order(request, order_id):
    """
    Handles the cancellation of a user's order with a confirmation step.
    Only unpaid orders can be cancelled.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.paid:
        messages.error(request, 'Cannot cancel an order that has already been paid.')
        return redirect('accounts:order_detail', order_id=order.id)

    if request.method == 'POST':
        order_id_copy = str(order.id)
        order.delete()
        messages.success(request, f"Order #{order_id_copy[:8]} has been successfully cancelled.")
        return redirect('accounts:profile')
    
    return render(request, 'accounts/delete_order_confirm.html', {'order': order})