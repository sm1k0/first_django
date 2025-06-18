from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shops.views import custom_404, custom_500

handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_store.urls')),  # Changed from 'api_shop.urls' to 'api_store.urls'
    path('', include('shops.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)