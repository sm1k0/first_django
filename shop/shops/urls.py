from django.urls import path
from . import views

urlpatterns = [
    # CRUD URLs
    path('categories/', views.CategoryCRUDView.as_view(), name='category_crud'),
    path('categories/<slug:slug>/', views.CategoryCRUDView.as_view(), name='category_crud'),
    path('products/', views.ProductCRUDView.as_view(), name='product_crud'),
    path('products/<slug:slug>/', views.ProductCRUDView.as_view(), name='product_crud'),
    path('customers/', views.CustomerCRUDView.as_view(), name='customer_crud'),
    path('customers/<int:pk>/', views.CustomerCRUDView.as_view(), name='customer_crud'),
    path('orders/', views.OrderCRUDView.as_view(), name='order_crud'),
    path('orders/<int:pk>/', views.OrderCRUDView.as_view(), name='order_crud'),
    path('reviews/', views.ReviewCRUDView.as_view(), name='review_crud'),
    path('reviews/<int:pk>/', views.ReviewCRUDView.as_view(), name='review_crud'),
    
    # Existing URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('find-us/', views.find_us, name='find_us'),
    path('products/', views.products, name='products'),
    path('categories/', views.categories, name='categories'),
    path('all-products/', views.all_products, name='all_products'),
    path('cart/', views.cart, name='cart'),
]