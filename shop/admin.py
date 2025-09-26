from django.contrib import admin
from .models import Category, Vendor, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('shop_name', 'user__username')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'price', 'stock_quantity', 'is_featured')
    list_filter = ('category', 'vendor', 'is_featured')
    search_fields = ('name', 'vendor__shop_name')
    prepopulated_fields = {'slug': ('name',)}