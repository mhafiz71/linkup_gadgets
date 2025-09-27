from django.shortcuts import render
from shop.models import Product, Category

def index(request):
    # Fetch featured products (limit to 4 for the main section)
    featured_products = Product.objects.filter(is_featured=True).order_by('-created_at')[:4]
    
    # Fetch new arrivals (latest 4 products)
    new_arrivals = Product.objects.all().order_by('-created_at')[:4]

    # THE FIX: Fetch only the first 4 categories
    categories = Category.objects.all()[:4]

    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)

# def shop(request):
#     return render(request, 'core/shop.html')

# def categories(request):
#     return render(request, 'core/categories.html')

# def sell_with_us(request):
#     return render(request, 'core/sell_with_us.html')

# def help_page(request):
#     return render(request, 'core/help.html')

# def about_us(request):
#     return render(request, 'core/about_us.html')

# def contact(request):
#     return render(request, 'core/contact.html')

# def vendors(request):
#     return render(request, 'core/vendors.html')

# def terms(request):
#     return render(request, 'core/terms.html')

def about_view(request):
    return render(request, 'core/about.html')

def terms_view(request):
    return render(request, 'core/terms.html')

def vendor_policies_view(request):
    return render(request, 'core/vendor_policies.html')

def faq_view(request):
    return render(request, 'core/faq.html')