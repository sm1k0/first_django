from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from shops.views import RegisterView

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include('shops.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)