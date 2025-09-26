from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import index, about_view, terms_view, vendor_policies_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', about_view, name='about'),
    path('terms/', terms_view, name='terms'),
    path('vendor-policies/', vendor_policies_view, name='vendor_policies'),
    path("__reload__/", include("django_browser_reload.urls")), # For live reload
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)