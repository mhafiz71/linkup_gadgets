from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Product, Category, Review, Vendor
from .forms import ProductForm, ReviewForm, VendorEditForm
from orders.models import OrderItem

def vendor_required(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'vendor'):
            return function(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap

def vendor_storefront(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    products = Product.objects.filter(vendor=vendor).order_by('-created_at')
    
    # Filter and sort options
    sort_by = request.GET.get('sort', 'featured')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:  # featured or default
        products = products.order_by('-is_featured', '-created_at')
    
    context = {
        'vendor': vendor,
        'products': products,
        'sort_by': sort_by,
    }
    return render(request, 'shop/vendor_storefront.html', context)

@login_required
@vendor_required
def vendor_dashboard(request):
    vendor = request.user.vendor
    order_items = OrderItem.objects.filter(product__vendor=vendor).order_by('-order__created_at')
    products = vendor.products.all()
    
    # Calculate dashboard statistics
    total_products = products.count()
    total_sales = order_items.filter(order__paid=True).count()
    total_revenue = sum(item.get_total_price() for item in order_items.filter(order__paid=True))
    low_stock_products = products.filter(stock_quantity__lte=5).count()
    
    # Recent orders (last 10)
    recent_orders = order_items.filter(order__paid=True)[:10]
    
    # Top selling products
    top_products = products.annotate(
        total_sold=Sum('order_items__quantity', filter=models.Q(order_items__order__paid=True))
    ).filter(total_sold__isnull=False).order_by('-total_sold')[:5]

    context = {
        'vendor': vendor,
        'order_items': order_items,
        'products': products,
        'total_products': total_products,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'top_products': top_products,
    }
    return render(request, 'shop/vendor_dashboard.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()
    new_review = None
    user_can_review = False
    
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        Q(id=product.id)
    ).order_by('?')[:4]
    
    
    if request.user.is_authenticated:
        if OrderItem.objects.filter(order__user=request.user, product=product).exists():
            user_can_review = True
        if Review.objects.filter(user=request.user, product=product).exists():
            user_can_review = False

    if request.method == 'POST' and user_can_review:
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.user = request.user
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
            product.vendor = request.user.vendor
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
    products_list = Product.objects.select_related('vendor', 'category').all()
    categories = Category.objects.all()
    selected_category_slug = request.GET.get('category')
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'featured')

    if selected_category_slug:
        products_list = products_list.filter(category__slug=selected_category_slug)
    
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(vendor__shop_name__icontains=query)
        )

    # Apply sorting
    if sort_by == 'price_low':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_high':
        products_list = products_list.order_by('-price')
    elif sort_by == 'newest':
        products_list = products_list.order_by('-created_at')
    elif sort_by == 'name':
        products_list = products_list.order_by('name')
    else:  # featured or default
        products_list = products_list.order_by('-is_featured', '-created_at')

    # Calculate statistics
    total_products = products_list.count()
    featured_products = products_list.filter(is_featured=True)[:4]
    
    paginator = Paginator(products_list, 12)  # Increased from 8 to 12
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'selected_category_slug': selected_category_slug,
        'query': query,
        'sort_by': sort_by,
        'total_products': total_products,
        'featured_products': featured_products,
    }
    return render(request, 'shop/shop_view.html', context)


@login_required
@vendor_required
def edit_vendor_info(request):
    vendor = request.user.vendor
    if request.method == 'POST':
        form = VendorEditForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your store information has been updated successfully!')
            return redirect('shop:vendor_dashboard')
    else:
        form = VendorEditForm(instance=vendor)

    return render(request, 'shop/vendor_info_edit.html', {'form': form})