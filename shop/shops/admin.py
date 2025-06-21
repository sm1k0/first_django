from django.contrib import admin
from .models import Category, Manufacturer, Product, Customer, Order, OrderItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image']
    list_filter = ['name']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_filter = ['country']
    search_fields = ['name', 'country']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'category', 'manufacturer']
    list_filter = ['category', 'manufacturer']
    search_fields = ['name', 'description', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock']
    ordering = ['name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['email']
    ordering = ['first_name', 'last_name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'id']
    list_editable = ['status']
    ordering = ['-created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order']
    search_fields = ['product__name', 'order__id']
    ordering = ['order']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'customer__first_name', 'customer__last_name']
    ordering = ['-created_at']