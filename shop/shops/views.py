from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, Http404
from .forms import CategoryForm, ProductForm, CustomerForm, OrderForm, ReviewForm, ManufacturerForm, RegisterForm
from .utils import api_request

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class AdminMenuView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_menu.html'

class CategoryListView(AdminRequiredMixin, ListView):
    template_name = 'category_crud.html'
    context_object_name = 'categories'

    def get_queryset(self):
        data = api_request('GET', 'categories/', self.request)
        return data['results'] if data else []

class CategoryCreateView(AdminRequiredMixin, CreateView):
    template_name = 'category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_crud')

    def form_valid(self, form):
        response = api_request('POST', 'categories/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Категория создана.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания категории.')
        return self.form_invalid(form)

class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_crud')

    def get_object(self):
        slug = self.kwargs['slug']
        data = api_request('GET', f'categories/{slug}/', self.request)
        if not data:
            raise Http404
        return data

    def get_initial(self):
        return self.get_object()

    def form_valid(self, form):
        slug = self.kwargs['slug']
        response = api_request('PATCH', f'categories/{slug}/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Категория обновлена.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка обновления категории.')
        return self.form_invalid(form)

class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    success_url = reverse_lazy('category_crud')

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        response = api_request('DELETE', f'categories/{slug}/', request)
        if response is None:
            messages.success(request, 'Категория удалена.')
            return redirect(self.success_url)
        messages.error(request, 'Ошибка удаления категории.')
        return redirect(self.success_url)

class ProductListView(AdminRequiredMixin, ListView):
    template_name = 'product_crud.html'
    context_object_name = 'products'

    def get_queryset(self):
        data = api_request('GET', 'products/', self.request)
        return data['results'] if data else []

class ProductCreateView(AdminRequiredMixin, CreateView):
    template_name = 'product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = api_request('POST', 'products/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Продукт создан.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания продукта.')
        return self.form_invalid(form)

class ProductUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_crud')

    def get_object(self):
        slug = self.kwargs['slug']
        data = api_request('GET', f'products/{slug}/', self.request)
        if not data:
            raise Http404
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        return self.get_object()

    def form_valid(self, form):
        slug = self.kwargs['slug']
        response = api_request('PATCH', f'products/{slug}/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Продукт обновлен.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка обновления продукта.')
        return self.form_invalid(form)

class ProductDeleteView(AdminRequiredMixin, DeleteView):
    success_url = reverse_lazy('product_crud')

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        response = api_request('DELETE', f'products/{slug}/', request)
        if response is None:
            messages.success(request, 'Продукт удален.')
            return redirect(self.success_url)
        messages.error(request, 'Ошибка удаления продукта.')
        return redirect(self.success_url)

class ManufacturerCreateView(AdminRequiredMixin, CreateView):
    template_name = 'manufacturer_form.html'
    form_class = ManufacturerForm
    success_url = reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        response = api_request('POST', 'manufacturers/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Производитель создан.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания производителя.')
        return self.form_invalid(form)

class ManufacturerUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'manufacturer_form.html'
    form_class = ManufacturerForm
    success_url = reverse_lazy('admin_dashboard')

    def get_object(self):
        pk = self.kwargs['pk']
        data = api_request('GET', f'manufacturers/{pk}/', self.request)
        if not data:
            raise Http404
        return data

    def get_initial(self):
        return self.get_object()

    def form_valid(self, form):
        pk = self.kwargs['pk']
        response = api_request('PATCH', f'manufacturers/{pk}/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Производитель обновлен.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка обновления производителя.')
        return self.form_invalid(form)

class ManufacturerDeleteView(AdminRequiredMixin, DeleteView):
    success_url = reverse_lazy('admin_dashboard')

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        response = api_request('DELETE', f'manufacturers/{pk}/', request)
        if response is None:
            messages.success(request, 'Производитель удален.')
            return redirect(self.success_url)
        messages.error(request, 'Ошибка удаления производителя.')
        return redirect(self.success_url)

class CustomerListView(AdminRequiredMixin, ListView):
    template_name = 'customer_crud.html'
    context_object_name = 'customers'

    def get_queryset(self):
        data = api_request('GET', 'customers/', self.request)
        return data['results'] if data else []

class CustomerCreateView(AdminRequiredMixin, CreateView):
    template_name = 'customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_crud')

    def form_valid(self, form):
        response = api_request('POST', 'customers/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Покупатель создан.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания покупателя.')
        return self.form_invalid(form)

class CustomerUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_crud')

    def get_object(self):
        pk = self.kwargs['pk']
        data = api_request('GET', f'customers/{pk}/', self.request)
        if not data:
            raise Http404
        return data

    def get_initial(self):
        return self.get_object()

    def form_valid(self, form):
        pk = self.kwargs['pk']
        response = api_request('PATCH', f'customers/{pk}/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Покупатель обновлен.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка обновления покупателя.')
        return self.form_invalid(form)

class CustomerDeleteView(AdminRequiredMixin, DeleteView):
    success_url = reverse_lazy('customer_crud')

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        response = api_request('DELETE', f'customers/{pk}/', request)
        if response is None:
            messages.success(request, 'Покупатель удален.')
            return redirect(self.success_url)
        messages.error(request, 'Ошибка удаления покупателя.')
        return redirect(self.success_url)

class OrderListView(AdminRequiredMixin, ListView):
    template_name = 'order_crud.html'
    context_object_name = 'orders'

    def get_queryset(self):
        data = api_request('GET', 'orders/', self.request)
        return data['results'] if data else []

class OrderCreateView(AdminRequiredMixin, CreateView):
    template_name = 'order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = api_request('POST', 'orders/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Заказ создан.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания заказа.')
        return self.form_invalid(form)

class OrderUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_crud')

    def get_object(self):
        pk = self.kwargs['pk']
        data = api_request('GET', f'orders/{pk}/', self.request)
        if not data:
            raise Http404
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        return self.get_object()

    def form_valid(self, form):
        pk = self.kwargs['pk']
        response = api_request('PATCH', f'orders/{pk}/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Заказ обновлен.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка обновления заказа.')
        return self.form_invalid(form)

class OrderDeleteView(AdminRequiredMixin, DeleteView):
    success_url = reverse_lazy('order_crud')

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        response = api_request('DELETE', f'orders/{pk}/', request)
        if response is None:
            messages.success(request, 'Заказ удален.')
            return redirect(self.success_url)
        messages.error(request, 'Ошибка удаления заказа.')
        return redirect(self.success_url)

class ReviewListView(AdminRequiredMixin, ListView):
    template_name = 'review_crud.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        data = api_request('GET', 'reviews/', self.request)
        return data['results'] if data else []

class ReviewCreateView(AdminRequiredMixin, CreateView):
    template_name = 'review_form.html'
    form_class = ReviewForm
    success_url = reverse_lazy('review_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = api_request('POST', 'reviews/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Отзыв создан.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания отзыва.')
        return self.form_invalid(form)

class ReviewUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'review_form.html'
    form_class = ReviewForm
    success_url = reverse_lazy('review_crud')

    def get_object(self):
        pk = self.kwargs['pk']
        data = api_request('GET', f'reviews/{pk}/', self.request)
        if not data:
            raise Http404
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        return self.get_object()

    def form_valid(self, form):
        pk = self.kwargs['pk']
        response = api_request('PATCH', f'reviews/{pk}/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Отзыв обновлен.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка обновления отзыва.')
        return self.form_invalid(form)

class ReviewDeleteView(AdminRequiredMixin, DeleteView):
    success_url = reverse_lazy('review_crud')

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        response = api_request('DELETE', f'reviews/{pk}/', request)
        if response is None:
            messages.success(request, 'Отзыв удален.')
            return redirect(self.success_url)
        messages.error(request, 'Ошибка удаления отзыва.')
        return redirect(self.success_url)

class UserManagementView(AdminRequiredMixin, ListView):
    template_name = 'user_management.html'
    context_object_name = 'users'
    queryset = User.objects.all()

class UserCreateView(AdminRequiredMixin, CreateView):
    template_name = 'user_form.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user_management')

    def form_valid(self, form):
        user = form.save()
        if user:
            messages.success(self.request, 'Пользователь создан.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания пользователя.')
        return self.form_invalid(form)

class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user_management')

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_staff or user.is_superuser:
            messages.error(request, 'Нельзя удалить администратора.')
            return redirect(self.success_url)
        user.delete()
        messages.success(request, 'Пользователь удален.')
        return redirect(self.success_url)

@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if not request.user.is_staff and request.user != user:
        messages.error(request, 'У вас нет прав для редактирования этого пользователя.')
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные пользователя обновлены.')
            return redirect('user_management')
        messages.error(request, 'Ошибка обновления данных.')
    else:
        form = RegisterForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        print("RegisterView: Form data:", form.cleaned_data)  # Отладка
        user = form.save()
        if user:
            # Создаем профиль покупателя без токена
            customer_data = {
                'user': user.id,
                'first_name': form.cleaned_data['username'],
                'last_name': '',
                'email': form.cleaned_data['email'],
                'phone': ''
            }
            print("Customer data:", customer_data)  # Отладка
            response = api_request('POST', 'customers/', self.request, data=customer_data)
            print("Customer API response:", response)  # Отладка
            if response:
                messages.success(self.request, 'Регистрация успешна. Пожалуйста, войдите.')
                return redirect(self.success_url)
            user.delete()
            messages.error(self.request, 'Ошибка создания профиля покупателя.')
        else:
            messages.error(self.request, 'Ошибка регистрации.')
        return self.form_invalid(form)
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print("POST data:", request.POST)  # Отладка
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Username: {username}, Password: {password}")  # Отладка
            # Прямой API-запрос для отладки
            import requests
            api_url = 'http://127.0.0.1:8000/api/auth/login/'
            api_data = {'username': username, 'password': password}
            print("API request data:", api_data)  # Отладка
            try:
                api_response = requests.post(api_url, json=api_data)
                print("API raw response:", api_response.status_code, api_response.text)  # Отладка
                response_data = api_response.json()
            except Exception as e:
                print("API request error:", str(e))  # Отладка
                response_data = None
            # Используем api_request как раньше
            response = api_request('POST', 'auth/login/', request, data=api_data)
            print("api_request response:", response)  # Отладка
            if response and 'token' in response:
                request.session['api_token'] = response['token']
                user = authenticate(request, username=username, password=password)
                print("Django auth user:", user)  # Отладка
                if user:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли.')
                    return redirect('home')
                else:
                    messages.error(request, 'Ошибка аутентификации.')
            else:
                messages.error(request, 'Неверные учетные данные.')
        else:
            print("Form errors:", form.errors)  # Отладка
            messages.error(request, 'Ошибка в данных формы.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def custom_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'Вы успешно вышли из аккаунта.')
    return redirect('login')

class AllProductsView(TemplateView):
    template_name = 'all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_data = api_request('GET', 'products/', self.request)
        context['products'] = products_data['results'] if products_data else []
        return context

def home(request):
    popular_products_data = api_request('GET', 'products/?ordering=-stock&page_size=3', request)
    popular_products = popular_products_data['results'] if popular_products_data else []
    return render(request, 'home.html', {'popular_products': popular_products})

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

def find_us(request):
    return render(request, 'find_us.html')

def products(request):
    return render(request, 'products.html')

def categories(request):
    categories_data = api_request('GET', 'categories/', request)
    categories = categories_data['results'] if categories_data else []
    return render(request, 'categories.html', {'categories': categories})

def category_products(request, slug):
    category_data = api_request('GET', f'categories/{slug}/', request)
    if not category_data:
        raise Http404
    products_data = api_request('GET', f'products/?category={category_data["id"]}', request)
    products = products_data['results'] if products_data else []
    return render(request, 'category_products.html', {'category': category_data, 'products': products})

def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Пожалуйста, авторизуйтесь для просмотра корзины.')
        return redirect('login')
    
    cart = request.session.get('cart', {})
    product_ids = list(cart.keys())
    if not product_ids:
        return render(request, 'cart.html', {'cart_items': [], 'total_price': 0})
    
    products_data = api_request('GET', f'products/?ids={",".join(product_ids)}', request)
    products = products_data['results'] if products_data else []
    
    cart_items = []
    total_price = 0
    for product in products:
        product_id = str(product['id'])
        if product_id in cart:
            quantity = cart[product_id]
            subtotal = float(product['price']) * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product_data = api_request('GET', f'products/{product_id}/', request)
    if not product_data or product_data['stock'] < 1:
        messages.error(request, 'Товара нет в наличии.')
        return redirect('all_products')
    
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f"{product_data['name']} добавлен в корзину.")
    return redirect('cart')

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        product_data = api_request('GET', f'products/{product_id}/', request)
        if not product_data:
            messages.error(request, 'Товар не найден.')
            return redirect('cart')
        
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        if quantity > product_data['stock']:
            messages.error(request, f'Недостаточно товара {product_data["name"]} на складе.')
            return redirect('cart')
        
        cart = request.session.get('cart', {})
        cart[str(product_id)] = quantity
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'Количество товара {product_data["name"]} обновлено.')
        return redirect('cart')
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'Товар удален из корзины.')
    return redirect('cart')

@login_required
def create_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Корзина пуста.')
        return redirect('cart')
    
    customer_data = api_request('GET', f'customers/?email={request.user.email}', request)
    if not customer_data or not customer_data['results']:
        messages.error(request, 'Пожалуйста, обновите данные профиля.')
        return redirect('cart')
    customer_id = customer_data['results'][0]['id']

    order_data = {'customer': customer_id, 'status': 'pending'}
    order_response = api_request('POST', 'orders/', request, data=order_data)
    if not order_response:
        messages.error(request, 'Ошибка создания заказа.')
        return redirect('cart')
    
    order_id = order_response['id']
    total_price = 0
    for product_id, quantity in cart.items():
        product_data = api_request('GET', f'products/{product_id}/', request)
        if not product_data or product_data['stock'] < quantity:
            messages.error(request, f'Недостаточно товара {product_data["name"]} на складе.')
            api_request('DELETE', f'orders/{order_id}/', request)
            return redirect('cart')
        
        subtotal = float(product_data['price']) * quantity
        order_item_data = {
            'order': order_id,
            'product': product_id,
            'quantity': quantity,
            'price': subtotal
        }
        api_request('POST', 'order-items/', request, data=order_item_data)
        
        product_update_data = {'stock': product_data['stock'] - quantity}
        api_request('PATCH', f'products/{product_id}/', request, data=product_update_data)
        total_price += subtotal
    
    del request.session['cart']
    request.session.modified = True
    messages.success(request, f'Заказ #{order_id} успешно создан.')
    return redirect('home')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)