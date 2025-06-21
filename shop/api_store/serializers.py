from rest_framework import serializers
from shops.models import Category, Product, Manufacturer, Customer, Order, OrderItem, Review
from django.contrib.auth.models import User
from rest_framework import serializers
from shops.models import Category, Product, Manufacturer, Customer, Order, OrderItem, Review
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'category', 'manufacturer', 'main_image']  # Исправлено 'image' на 'main_image'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country']  # Исправлено 'description' на 'country'

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone']

    def validate(self, data):
        print("CustomerSerializer: Validating data:", data)
        return data

    def create(self, validated_data):
        print("CustomerSerializer: Creating with validated data:", validated_data)
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at']