from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('callback/', views.payment_callback, name='callback'),
    path('failed/', views.payment_failed, name='failed'),
    path('retry/<uuid:order_id>/', views.retry_payment, name='retry_payment'),
]