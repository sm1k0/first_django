from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .serializers import (
    CategorySerializer, ProductSerializer, ManufacturerSerializer,
    CustomerSerializer, OrderSerializer, OrderItemSerializer, ReviewSerializer
)
from shops.models import (
    Category, Product, Manufacturer, Customer, Order, OrderItem, Review
)
from .pagination import CustomPagination
from .permissions import IsViewAndEditOnly, IsViewAndDeleteOnly, IsViewAndDeleteOnlyRole3

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsViewAndEditOnly() | IsViewAndDeleteOnly() | IsViewAndDeleteOnlyRole3()]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))
        return queryset

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsViewAndEditOnly() | IsViewAndDeleteOnly() | IsViewAndDeleteOnlyRole3()]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
        return queryset

class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all().order_by('id')
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAuthenticated, IsViewAndEditOnly | IsViewAndDeleteOnly | IsViewAndDeleteOnlyRole3]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'country']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(country__icontains=search_query)
            )
        return queryset

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsViewAndEditOnly | IsViewAndDeleteOnly | IsViewAndDeleteOnlyRole3]
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

    def create(self, request, *args, **kwargs):
        print("CustomerViewSet: Create request data:", request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print("CustomerViewSet: Validated data:", serializer.validated_data)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print("CustomerViewSet: Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
    # Измените permission_classes для POST-запросов
    permission_classes = [AllowAny]  # Начальное значение для совместимости
    filter_backends = [SearchFilter]
    search_fields = ['status']

    def get_permissions(self):
        # Разрешить всем аутентифицированным пользователям для POST, остальные методы ограничены
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # Только аутентификация для создания заказов
        return [IsAuthenticated(), IsViewAndEditOnly() | IsViewAndDeleteOnly() | IsViewAndDeleteOnlyRole3()]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(status__icontains=search_query))
        return queryset

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all().order_by('id')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsViewAndEditOnly | IsViewAndDeleteOnly | IsViewAndDeleteOnlyRole3]
    filter_backends = [SearchFilter]
    search_fields = ['product__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(product__name__icontains=search_query))
        return queryset

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsViewAndEditOnly | IsViewAndDeleteOnly | IsViewAndDeleteOnlyRole3]
    filter_backends = [SearchFilter]
    search_fields = ['comment']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(comment__icontains=search_query))
        return queryset

class AuthLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print("AuthLoginView: Request data:", request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"AuthLoginView: Username: {username}, Password: {password}")
        if not username or not password:
            return Response({'detail': 'Учетные данные не были предоставлены.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(request, username=username, password=password)
        print(f"AuthLoginView: Authenticated user: {user}")
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            request.session['api_token'] = token.key
            request.session.modified = True
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

class AuthLogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print("AuthLogoutView: User:", request.user)
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            request.session.flush()
            logout(request)
            return Response({'message': 'Выход выполнен'}, status=status.HTTP_200_OK)
        return Response({'error': 'Не аутентифицирован'}, status=status.HTTP_401_UNAUTHORIZED)