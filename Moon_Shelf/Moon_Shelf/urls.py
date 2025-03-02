from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('books', include('shop.urls')),
    path('basket', include('shop.urls')),
    path('orders', include('shop.urls')),
    path('profile', include('shop.urls')),
    path('stock', include('shop.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
