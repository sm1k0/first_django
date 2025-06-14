from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Category, Product, Customer, Order, Review, Manufacturer, OrderItem
from .forms import CategoryForm, ProductForm, CustomerForm, OrderForm, ReviewForm, ManufacturerForm, RegisterForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class AdminMenuView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'admin_menu.html'

class CategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Category
    template_name = 'category_crud.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryForm()
        context['edit_category'] = None
        return context

class CategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_crud.html'
    success_url = reverse_lazy('category_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Категория сохранена.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме категории.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['edit_category'] = None
        return context

class CategoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_crud.html'
    success_url = reverse_lazy('category_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Категория сохранена.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме категории.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['edit_category'] = self.get_object()
        return context

class CategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Категория удалена.')
        return super().form_valid(form)

class ProductListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Product
    template_name = 'product_crud.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manufacturers'] = Manufacturer.objects.all()
        context['product_form'] = ProductForm()
        context['manufacturer_form'] = ManufacturerForm()
        context['edit_product'] = None
        context['edit_manufacturer'] = None
        return context

class ProductCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_crud.html'
    success_url = reverse_lazy('product_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Товар сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме товара.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['manufacturers'] = Manufacturer.objects.all()
        context['product_form'] = self.get_form()
        context['manufacturer_form'] = ManufacturerForm()
        context['edit_product'] = None
        context['edit_manufacturer'] = None
        return context

class ProductUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_crud.html'
    success_url = reverse_lazy('product_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Товар сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме товара.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['manufacturers'] = Manufacturer.objects.all()
        context['product_form'] = self.get_form()
        context['manufacturer_form'] = ManufacturerForm()
        context['edit_product'] = self.get_object()
        context['edit_manufacturer'] = None
        return context

class ProductDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Товар удален.')
        return super().form_valid(form)

class ManufacturerCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'product_crud.html'
    success_url = reverse_lazy('product_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Производитель сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме производителя.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['manufacturers'] = Manufacturer.objects.all()
        context['product_form'] = ProductForm()
        context['manufacturer_form'] = self.get_form()
        context['edit_product'] = None
        context['edit_manufacturer'] = None
        return context

class ManufacturerUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'product_crud.html'
    success_url = reverse_lazy('product_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Производитель сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме производителя.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['manufacturers'] = Manufacturer.objects.all()
        context['product_form'] = ProductForm()
        context['manufacturer_form'] = self.get_form()
        context['edit_product'] = None
        context['edit_manufacturer'] = self.get_object()
        return context

class ManufacturerDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Manufacturer
    success_url = reverse_lazy('product_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Производитель удален.')
        return super().form_valid(form)

class CustomerListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Customer
    template_name = 'customer_crud.html'
    context_object_name = 'customers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomerForm()
        context['edit_customer'] = None
        return context

class CustomerCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer_crud.html'
    success_url = reverse_lazy('customer_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Покупатель сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме покупателя.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        context['edit_customer'] = None
        return context

class CustomerUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer_crud.html'
    success_url = reverse_lazy('customer_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Покупатель сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме покупателя.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        context['edit_customer'] = self.get_object()
        return context

class CustomerDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customer_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Покупатель удален.')
        return super().form_valid(form)

class OrderListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Order
    template_name = 'order_crud.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm()
        context['edit_order'] = None
        return context

class OrderCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_crud.html'
    success_url = reverse_lazy('order_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Заказ сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме заказа.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['edit_order'] = None
        return context

class OrderUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_crud.html'
    success_url = reverse_lazy('order_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Заказ сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме заказа.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['edit_order'] = self.get_object()
        return context

class OrderDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Заказ удален.')
        return super().form_valid(form)

class ReviewListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Review
    template_name = 'review_crud.html'
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        context['edit_review'] = None
        return context

class ReviewCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_crud.html'
    success_url = reverse_lazy('review_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Отзыв сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме отзыва.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.all()
        context['edit_review'] = None
        return context

class ReviewUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_crud.html'
    success_url = reverse_lazy('review_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Отзыв сохранен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме отзыва.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.all()
        context['edit_review'] = self.get_object()
        return context

class ReviewDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('review_crud')

    def form_valid(self, form):
        messages.success(self.request, 'Отзыв удален.')
        return super().form_valid(form)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        Customer.objects.create(
            user=user,
            first_name=user.username,
            last_name='',
            email=user.email,
            phone=''
        )
        messages.success(self.request, 'Регистрация успешна. Пожалуйста, войдите.')
        return super().form_valid(form)

class AllProductsView(ListView):
    template_name = 'all_products.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context

class UserManagementView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'user_management.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterForm()
        return context

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    form_class = RegisterForm
    template_name = 'user_management.html'
    success_url = reverse_lazy('user_management')

    def form_valid(self, form):
        user = form.save()
        Customer.objects.create(
            user=user,
            first_name=user.username,
            last_name='',
            email=user.email,
            phone=''
        )
        messages.success(self.request, 'Пользователь создан.')
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user_management')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь удален.')
        return super().form_valid(form)

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.is_staff)
def user_update(request, pk):
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=pk)
            customer = user.customer
            data = request.POST.dict()
            
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
                customer.email = data['email']
            if 'first_name' in data:
                customer.first_name = data['first_name']
            if 'last_name' in data:
                customer.last_name = data['last_name']
            if 'phone' in data:
                customer.phone = data['phone']
            if 'is_staff' in data:
                user.is_staff = data['is_staff'].lower() == 'true'
            if 'is_active' in data:
                user.is_active = data['is_active'].lower() == 'true'

            user.save()
            customer.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def home(request):
    popular_products = Product.objects.order_by('-stock')[:3]
    return render(request, 'home.html', {'request': request, 'popular_products': popular_products})

def about(request):
    return render(request, 'about.html', {'request': request})

def contacts(request):
    return render(request, 'contacts.html', {'request': request})

def find_us(request):
    return render(request, 'find_us.html', {'request': request})

def products(request):
    return render(request, 'products.html', {'request': request})

def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'request': request, 'categories': categories})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {'request': request, 'category': category, 'products': products})

def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Пожалуйста, авторизуйтесь для просмотра корзины.')
        return redirect('login')
    
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        total_price += product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': product.price * quantity})
    return render(request, 'cart.html', {'request': request, 'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock < 1:
        messages.error(request, 'Товара нет в наличии.')
        return redirect('all_products')
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'{product.name} добавлен в корзину.')
    return redirect('cart')

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        if quantity > product.stock:
            messages.error(request, f'Недостаточно товара {product.name} на складе.')
            return redirect('cart')
        cart = request.session.get('cart', {})
        cart[str(product_id)] = quantity
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'Количество товара {product.name} обновлено.')
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
    
    try:
        customer = Customer.objects.get(email=request.user.email)
    except Customer.DoesNotExist:
        messages.error(request, 'Пожалуйста, обновите данные профиля.')
        return redirect('cart')

    order = Order.objects.create(customer=customer, status='pending')
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        if product.stock < quantity:
            messages.error(request, f'Недостаточно товара {product.name} на складе.')
            order.delete()
            return redirect('cart')
        product.stock -= quantity
        product.save()
        subtotal = product.price * quantity
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=subtotal)
        total_price += subtotal
    
    del request.session['cart']
    request.session.modified = True
    messages.success(request, f'Заказ #{order.id} успешно создан.')
    return redirect('home')

def custom_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'Вы успешно вышли из аккаунта.')
    return redirect('login')  # Перенаправление на страницу логина
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

class OrderManagementView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Order
    template_name = 'order_management.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all().prefetch_related('orderitem_set__product')
        return context