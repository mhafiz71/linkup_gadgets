from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review
from orders.models import OrderItem
from .forms import ProductForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ProductForm, ReviewForm, VendorEditForm
from django.contrib import messages
from .models import Product, Category, Vendor # Add Vendor

# A simple decorator to check if the user is a vendor
def vendor_required(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'vendor'):
            return function(request, *args, **kwargs)
        else:
            return redirect('index') # Or a "permission denied" page
    return wrap

def vendor_storefront(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    products = Product.objects.filter(vendor=vendor)
    context = {
        'vendor': vendor,
        'products': products,
    }
    return render(request, 'shop/vendor_storefront.html', context)

@login_required
@vendor_required
def vendor_dashboard(request):
    vendor = request.user.vendor
    # Get all order items related to this vendor's products
    order_items = OrderItem.objects.filter(product__vendor=vendor)
    products = vendor.products.all()

    context = {
        'vendor': vendor,
        'order_items': order_items,
        'products': products
    }
    return render(request, 'shop/vendor_dashboard.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()
    
    # Review form logic
    new_review = None
    user_can_review = False
    
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        Q(id=product.id)
    ).order_by('?')[:4]
    
    
    if request.user.is_authenticated:
        # Check if the user has purchased this product
        if OrderItem.objects.filter(order__user=request.user, product=product).exists():
            user_can_review = True
        # Check if the user has already reviewed this product
        if Review.objects.filter(user=request.user, product=product).exists():
            user_can_review = False # Already reviewed, so can't review again

    if request.method == 'POST' and user_can_review:
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            # Create Review object but don't save to database yet
            new_review = review_form.save(commit=False)
            # Assign the current product and user to the review
            new_review.product = product
            new_review.user = request.user
            # Save the review to the database
            new_review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('shop:product_detail', slug=product.slug)
    else:
        review_form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'user_can_review': user_can_review,
        'related_products': related_products,        
    }
    return render(request, 'shop/product_detail.html', context)

@login_required
@vendor_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor # Automatically assign the vendor
            product.save()
            return redirect('shop:vendor_dashboard')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

@login_required
@vendor_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, vendor=request.user.vendor)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:vendor_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form})

@login_required
@vendor_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, vendor=request.user.vendor)
    if request.method == 'POST':
        product.delete()
        return redirect('shop:vendor_dashboard')
    return render(request, 'shop/delete_confirm.html', {'product': product})

def shop_view(request):
    # Start with all products
    products_list = Product.objects.all()
    categories = Category.objects.all()
    
    # Get query parameters
    selected_category_slug = request.GET.get('category')
    query = request.GET.get('q')

    # Filter by category
    if selected_category_slug:
        products_list = products_list.filter(category__slug=selected_category_slug)
    
    # Filter by search query
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Set up pagination
    paginator = Paginator(products_list, 8) # Show 8 products per page
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'selected_category_slug': selected_category_slug,
        'query': query,
    }
    return render(request, 'shop/shop_view.html', context)


@login_required
@vendor_required
def edit_vendor_info(request):
    vendor = request.user.vendor
    if request.method == 'POST':
        # Remember request.FILES for image uploads
        form = VendorEditForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your store information has been updated successfully!')
            return redirect('shop:vendor_dashboard')
    else:
        form = VendorEditForm(instance=vendor)

    return render(request, 'shop/vendor_info_edit.html', {'form': form})