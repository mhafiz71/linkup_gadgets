from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from orders.models import Order, OrderItem
from django.db import transaction
from .forms import UserRegisterForm, VendorRegisterForm
from django.contrib.auth.decorators import login_required

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
                # Redirect to a dashboard or homepage
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