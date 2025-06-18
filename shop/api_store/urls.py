from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ManufacturerViewSet,
    CustomerViewSet, OrderViewSet, OrderItemViewSet, ReviewViewSet,
    AuthLoginView, AuthLogoutView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('auth/login/', AuthLoginView.as_view(), name='api_auth_login'),
    path('auth/logout/', AuthLogoutView.as_view(), name='api_auth_logout'),
] + router.urls