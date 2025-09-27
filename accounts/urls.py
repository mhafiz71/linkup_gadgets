from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.customer_profile, name='profile'),
    path('profile/order/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('profile/order/<uuid:order_id>/delete/', views.delete_order, name='delete_order'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]