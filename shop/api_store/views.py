from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from .serializers import (
    CategorySerializer, ProductSerializer, ManufacturerSerializer,
    CustomerSerializer, OrderSerializer, OrderItemSerializer, ReviewSerializer
)
from shops.models import (
    Category, Product, Manufacturer, Customer, Order, OrderItem, Review
)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all().order_by('id')
    serializer_class = ManufacturerSerializer
    permission_classes = [AllowAny]

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]  # Разрешить создание без токена

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all().order_by('id')
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

class AuthLoginView(APIView):
    permission_classes = [AllowAny]  # Отключить требования аутентификации
    def post(self, request):
        print("Request data:", request.data)  # Отладка
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Username: {username}, Password: {password}")  # Отладка
        user = authenticate(request, username=username, password=password)
        print(f"Authenticated user: {user}")  # Отладка
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

class AuthLogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({'message': 'Выход выполнен'}, status=status.HTTP_200_OK)
        return Response({'error': 'Не аутентифицирован'}, status=status.HTTP_401_UNAUTHORIZED)