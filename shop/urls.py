from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.shop_view, name='shop_view'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('dashboard/add-product/', views.add_product, name='add_product'),
    path('dashboard/edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('dashboard/delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
]