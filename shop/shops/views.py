from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from .forms import CategoryForm, ProductForm, CustomerForm, OrderForm, ReviewForm, ManufacturerForm, RegisterForm
from .utils import api_request
import requests

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class AdminMenuView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_menu.html'

class CategoryListView(AdminRequiredMixin, ListView):
    template_name = 'category_crud.html'
    context_object_name = 'categories'

    def get_queryset(self):
        print(f"CategoryListView: User: {self.request.user}, Is staff: {self.request.user.is_staff}")
        data = api_request('GET', 'categories/', self.request)
        print(f"CategoryListView: API response: {data}")
        return data['results'] if data else []
class CategoryCreateView(AdminRequiredMixin, CreateView):
    template_name = 'category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_crud')

    def get_form(self, form_class=None):
        return self.form_class()

    def form_valid(self, form):
        print(f"CategoryCreateView: Form data: {form.cleaned_data}")
        data = form.cleaned_data.copy()
        files = None
        if 'image' in data and data['image']:
            files = {'image': (data['image'].name, data['image'].file, data['image'].content_type)}
            del data['image']  # Удаляем image из data, так как оно отправляется как файл
        response = api_request('POST', 'categories/', self.request, data=data, files=files)
        print(f"CategoryCreateView: API response: {response}")
        if response:
            messages.success(self.request, 'Категория создана.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания категории.')
        return self.form_invalid(form)

class ProductCreateView(AdminRequiredMixin, CreateView):
    template_name = 'product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        if 'instance' in kwargs:
            del kwargs['instance']
        return kwargs

    def form_valid(self, form):
        print(f"ProductCreateView: Form data: {form.cleaned_data}")
        data = form.cleaned_data.copy()
        files = None
        if 'main_image' in data and data['main_image']:
            files = {'main_image': (data['main_image'].name, data['main_image'].file, data['main_image'].content_type)}
            del data['main_image']  # Удаляем main_image из data, так как оно отправляется как файл
        response = api_request('POST', 'products/', self.request, data=data, files=files)
        print(f"ProductCreateView: API response: {response}")
        if response:
            messages.success(self.request, 'Продукт создан.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания продукта.')
        return self.form_invalid(form)
class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_crud')

    def get_object(self):
        slug = self.kwargs['slug']
        data = api_request('GET', f'categories/?slug={slug}', self.request)
        if not data or not data['results']:
            raise Http404
        return data['results'][0]

    def get_form(self, form_class=None):
        return self.form_class(initial=self.get_initial())

    def get_initial(self):
        return self.get_object()

    def form_valid(self, form):
        slug = self.kwargs['slug']
        category_data = api_request('GET', f'categories/?slug={slug}', self.request)
        if not category_data or not category_data['results']:
            raise Http404
        category_id = category_data['results'][0]['id']
        response = api_request('PATCH', f'categories/{category_id}/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Категория обновлена.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка обновления категории.')
        return self.form_invalid(form)

class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    success_url = reverse_lazy('category_crud')

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category_data = api_request('GET', f'categories/?slug={slug}', request)
        if not category_data or not category_data['results']:
            messages.error(request, 'Категория не найдена.')
            return redirect(self.success_url)
        category_id = category_data['results'][0]['id']
        response = api_request('DELETE', f'categories/{category_id}/', request)
        if response is None:
            messages.success(request, 'Категория удалена.')
        else:
            messages.error(request, 'Ошибка удаления категории.')
        return redirect(self.success_url)

class ProductListView(AdminRequiredMixin, ListView):
    template_name = 'product_crud.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manufacturers_data = api_request('GET', 'manufacturers/', self.request)
        context['manufacturers'] = manufacturers_data['results'] if manufacturers_data else []
        print(f"ProductListView: User: {self.request.user}, Is staff: {self.request.user.is_staff}")
        print(f"ProductListView: Manufacturers: {context['manufacturers']}")
        return context

    def get_queryset(self):
        print(f"ProductListView: Fetching products")
        data = api_request('GET', 'products/', self.request)
        print(f"ProductListView: API response: {data}")
        return data['results'] if data else []


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_crud')

    def get_object(self):
        slug = self.kwargs['slug']
        data = api_request('GET', f'products/?slug={slug}', self.request)
        if not data or not data['results']:
            raise Http404
        return data['results'][0]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        return self.get_object()

    def form_valid(self, form):
        slug = self.kwargs['slug']
        product_data = api_request('GET', f'products/?slug={slug}', self.request)
        if not product_data or not product_data['results']:
            raise Http404
        product_id = product_data['results'][0]['id']
        response = api_request('PATCH', f'products/{product_id}/', self.request, data=form.cleaned_data)
        if response:
            messages.success(self.request, 'Продукт обновлен.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка обновления продукта.')
        return self.form_invalid(form)

class ProductDeleteView(AdminRequiredMixin, DeleteView):
    success_url = reverse_lazy('product_crud')

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        product_data = api_request('GET', f'products/?slug={slug}', request)
        if not product_data or not product_data['results']:
            messages.error(request, 'Продукт не найден.')
            return redirect(self.success_url)
        product_id = product_data['results'][0]['id']
        response = api_request('DELETE', f'products/{product_id}/', request)
        if response is None:
            messages.success(request, 'Продукт удален.')
        else:
            messages.error(request, 'Ошибка удаления продукта.')
        return redirect(self.success_url)

class ManufacturerCreateView(AdminRequiredMixin, CreateView):
    template_name = 'manufacturer_form.html'
    form_class = ManufacturerForm
    success_url = reverse_lazy('product_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'instance' in kwargs:
            del kwargs['instance']  # Удаляем instance
        return kwargs

    def form_valid(self, form):
        print(f"ManufacturerCreateView: Form data: {form.cleaned_data}")
        response = api_request('POST', 'manufacturers/', self.request, data=form.cleaned_data)
        print(f"ManufacturerCreateView: API response: {response}")
        if response:
            messages.success(self.request, 'Производитель создан.')
            return redirect(self.success_url)
        messages.error(self.request, 'Ошибка создания производителя.')
        return self.form_invalid(form)

class ManufacturerUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'manufacturer_form.html'
    form_class = ManufacturerForm
    success_url = reverse_lazy('product_crud')

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
    success_url = reverse_lazy('product_crud')

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        response = api_request('DELETE', f'manufacturers/{pk}/', request)
        if response is None:
            messages.success(request, 'Производитель удален.')
        else:
            messages.error(request, 'Ошибка удаления производителя.')
        return redirect(self.success_url)

class CustomerListView(AdminRequiredMixin, ListView):
    template_name = 'customer_crud.html'
    context_object_name = 'customers'

    def get_queryset(self):
        print(f"CustomerListView: User: {self.request.user}, Is staff: {self.request.user.is_staff}")
        data = api_request('GET', 'customers/', self.request)
        print(f"CustomerListView: API response: {data}")
        return data['results'] if data else []

class CustomerCreateView(AdminRequiredMixin, CreateView):
    template_name = 'customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'instance' in kwargs:
            del kwargs['instance']  # Удаляем instance
        return kwargs

    def form_valid(self, form):
        print(f"CustomerCreateView: Form data: {form.cleaned_data}")
        response = api_request('POST', 'customers/', self.request, data=form.cleaned_data)
        print(f"CustomerCreateView: API response: {response}")
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
        else:
            messages.error(request, 'Ошибка удаления покупателя.')
        return redirect(self.success_url)

class OrderListView(AdminRequiredMixin, ListView):
    template_name = 'order_crud.html'
    context_object_name = 'orders'

    def get_queryset(self):
        print(f"OrderListView: User: {self.request.user}, Is staff: {self.request.user.is_staff}")
        data = api_request('GET', 'orders/', self.request)
        print(f"OrderListView: API response: {data}")
        return data['results'] if data else []

class OrderCreateView(AdminRequiredMixin, CreateView):
    template_name = 'order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        if 'instance' in kwargs:
            del kwargs['instance']  # Удаляем instance
        return kwargs

    def form_valid(self, form):
        print(f"OrderCreateView: Form data: {form.cleaned_data}")
        response = api_request('POST', 'orders/', self.request, data=form.cleaned_data)
        print(f"OrderCreateView: API response: {response}")
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
        else:
            messages.error(request, 'Ошибка удаления заказа.')
        return redirect(self.success_url)

class ReviewListView(AdminRequiredMixin, ListView):
    template_name = 'review_crud.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        print(f"ReviewListView: User: {self.request.user}, Is staff: {self.request.user.is_staff}")
        data = api_request('GET', 'reviews/', self.request)
        print(f"ReviewListView: API response: {data}")
        return data['results'] if data else []

class ReviewCreateView(AdminRequiredMixin, CreateView):
    template_name = 'review_form.html'
    form_class = ReviewForm
    success_url = reverse_lazy('review_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        if 'instance' in kwargs:
            del kwargs['instance']  # Удаляем instance
        return kwargs

    def form_valid(self, form):
        print(f"ReviewCreateView: Form data: {form.cleaned_data}")
        response = api_request('POST', 'reviews/', self.request, data=form.cleaned_data)
        print(f"ReviewCreateView: API response: {response}")
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
        else:
            messages.error(request, 'Ошибка удаления отзыва.')
        return redirect(self.success_url)

class UserManagementView(AdminRequiredMixin, ListView):
    template_name = 'user_management.html'
    context_object_name = 'users'
    queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterForm()
        return context

class UserCreateView(AdminRequiredMixin, CreateView):
    template_name = 'user_form.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user_management')

    def form_valid(self, form):
        print(f"UserCreateView: Form data: {form.cleaned_data}")
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
        print(f"RegisterView: Form data: {form.cleaned_data}")
        user = form.save()
        if user:
            customer_data = {
                'user': user.id,
                'first_name': form.cleaned_data['username'],
                'last_name': '',
                'email': form.cleaned_data['email'],
                'phone': ''
            }
            print(f"RegisterView: Customer data: {customer_data}")
            response = api_request('POST', 'customers/', self.request, data=customer_data)
            print(f"RegisterView: Customer API response: {response}")
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
        print(f"custom_login: POST data: {request.POST}")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"custom_login: Username: {username}")
            api_data = {'username': username, 'password': password}
            print(f"custom_login: API request data: {api_data}")
            try:
                api_response = requests.post('http://127.0.0.1:8000/api/auth/login/', json=api_data)
                print(f"custom_login: API response: {api_response.status_code} {api_response.text}")
                response_data = api_response.json()
            except Exception as e:
                print(f"custom_login: API request error: {str(e)}")
                response_data = None
            response = api_request('POST', 'auth/login/', request, data=api_data)
            print(f"custom_login: api_request response: {response}")
            if response and 'token' in response:
                request.session['api_token'] = response['token']
                user = authenticate(request, username=username, password=password)
                print(f"custom_login: Django auth user: {user}")
                if user:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли.')
                    return redirect('home')
                messages.error(request, 'Ошибка аутентификации.')
            else:
                messages.error(request, 'Неверные учетные данные.')
        else:
            print(f"custom_login: Form errors: {form.errors}")
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
        search_query = self.request.GET.get('search', '')
        page_size = self.request.GET.get('page_size', 10)
        page = self.request.GET.get('page', 1)
        params = f'?page={page}&page_size={page_size}'
        if search_query:
            params += f'&search={search_query}'
        print(f"AllProductsView: Fetching products with params: {params}")
        products_data = api_request('GET', f'products/{params}', self.request)
        print(f"AllProductsView: API response: {products_data}")
        context['products'] = products_data.get('results', []) if products_data else []
        context['search_query'] = search_query
        context['page_size'] = page_size
        total_count = products_data.get('count', 0) if products_data else 0
        total_pages = (total_count + int(page_size) - 1) // int(page_size)
        current_page = int(page)
        range_start = max(1, current_page - 2)
        range_end = min(total_pages + 1, current_page + 3)
        context['pagination'] = {
            'count': total_count,
            'next': products_data.get('next') if products_data else None,
            'previous': products_data.get('previous') if products_data else None,
            'current_page': current_page,
            'range_pages': range(range_start, range_end),
        }
        return context   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        page_size = self.request.GET.get('page_size', 10)
        page = self.request.GET.get('page', 1)
        params = f'?page={page}&page_size={page_size}'
        if search_query:
            params += f'&search={search_query}'
        print(f"AllProductsView: Fetching products with params: {params}")
        products_data = api_request('GET', f'products/{params}', self.request)
        print(f"AllProductsView: API response: {products_data}")
        context['products'] = products_data.get('results', []) if products_data else []
        context['search_query'] = search_query
        context['page_size'] = page_size
        total_count = products_data.get('count', 0) if products_data else 0
        total_pages = (total_count + int(page_size) - 1) // int(page_size)
        current_page = int(page)
        range_start = max(1, current_page - 2)
        range_end = min(total_pages + 1, current_page + 3)
        context['pagination'] = {
            'count': total_count,
            'next': products_data.get('next') if products_data else None,
            'previous': products_data.get('previous') if products_data else None,
            'current_page': current_page,
            'range_pages': range(range_start, range_end),
        }
        return context
def home(request):
    print("home: Fetching popular products")
    popular_products_data = api_request('GET', 'products/?ordering=-stock&page_size=3', request)
    print(f"home: API response: {popular_products_data}")
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
    print("categories: Fetching categories")
    categories_data = api_request('GET', 'categories/', request)
    print(f"categories: API response: {categories_data}")
    categories = categories_data['results'] if categories_data else []
    return render(request, 'categories.html', {'categories': categories})

def category_products(request, slug):
    print(f"category_products: Fetching category with slug: {slug}")
    category_data = api_request('GET', f'categories/?slug={slug}', request)
    print(f"category_products: Category API response: {category_data}")
    if not category_data or not category_data['results']:
        raise Http404
    category = category_data['results'][0]
    products_data = api_request('GET', f'products/?category={category["id"]}', request)
    print(f"category_products: Products API response: {products_data}")
    products = products_data['results'] if products_data else []
    return render(request, 'category_products.html', {'category': category, 'products': products})

def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Пожалуйста, авторизуйтесь для просмотра корзины.')
        return redirect('login')
    
    cart = request.session.get('cart', {})
    product_ids = list(cart.keys())
    if not product_ids:
        return render(request, 'cart.html', {'cart_items': [], 'total_price': 0})
    
    print(f"cart: Fetching products with IDs: {product_ids}")
    products_data = api_request('GET', f'products/?ids={",".join(product_ids)}', request)
    print(f"cart: API response: {products_data}")
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
    print(f"add_to_cart: Fetching product with ID: {product_id}")
    product_data = api_request('GET', f'products/{product_id}/', request)
    print(f"add_to_cart: API response: {product_data}")
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
        print(f"update_cart: Fetching product with ID: {product_id}")
        product_data = api_request('GET', f'products/{product_id}/', request)
        print(f"update_cart: API response: {product_data}")
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
    
    print(f"create_order: Fetching customer with email: {request.user.email}")
    customer_data = api_request('GET', f'customers/?email={request.user.email}', request)
    print(f"create_order: Customer API response: {customer_data}")
    if not customer_data or not customer_data['results']:
        messages.error(request, 'Пожалуйста, обновите данные профиля.')
        return redirect('cart')
    customer_id = customer_data['results'][0]['id']

    order_data = {'customer': customer_id, 'status': 'pending'}
    print(f"create_order: Creating order with data: {order_data}")
    order_response = api_request('POST', 'orders/', request, data=order_data)
    print(f"create_order: Order API response: {order_response}")
    if not order_response:
        messages.error(request, 'Ошибка создания заказа.')
        return redirect('cart')
    
    order_id = order_response['id']
    total_price = 0
    for product_id, quantity in cart.items():
        print(f"create_order: Fetching product with ID: {product_id}")
        product_data = api_request('GET', f'products/{product_id}/', request)
        print(f"create_order: Product API response: {product_data}")
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
        print(f"create_order: Creating order item with data: {order_item_data}")
        api_request('POST', 'order-items/', request, data=order_item_data)
        
        product_update_data = {'stock': product_data['stock'] - quantity}
        print(f"create_order: Updating product stock with data: {product_update_data}")
        api_request('PATCH', f'products/{product_id}/', request, data=product_update_data)
        total_price += subtotal
    
    del request.session['cart']
    request.session.modified = True
    messages.success(request, f'Заказ #{order_id} успешно создан. Общая сумма: {total_price} руб.')
    return redirect('home')
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)