from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path("__reload__/", include("django_browser_reload.urls")), # For live reload
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)