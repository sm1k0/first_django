from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .utils import api_request

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название')
    slug = forms.SlugField(max_length=100, label='Slug')
    image = forms.ImageField(required=False, label='Изображение')

class ManufacturerForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название')
    country = forms.CharField(max_length=100, label='Страна')

class ProductForm(forms.Form):
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        categories_data = api_request('GET', 'categories/', request) if request else None
        manufacturers_data = api_request('GET', 'manufacturers/', request) if request else None
        self.fields['category'].choices = [(cat['id'], cat['name']) for cat in categories_data['results']] if categories_data else []
        self.fields['manufacturer'].choices = [('', '---------')] + [(man['id'], man['name']) for man in manufacturers_data['results']] if manufacturers_data else []

    name = forms.CharField(max_length=100, label='Название')
    slug = forms.SlugField(max_length=100, label='Slug')
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    price = forms.DecimalField(max_digits=10, decimal_places=2, label='Цена')
    stock = forms.IntegerField(label='Остаток')
    category = forms.ChoiceField(label='Категория')
    manufacturer = forms.ChoiceField(required=False, label='Производитель')
    main_image = forms.ImageField(required=False, label='Изображение')

class CustomerForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, required=False, label='Телефон')

class OrderForm(forms.Form):
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        customers_data = api_request('GET', 'customers/', request) if request else None
        self.fields['customer'].choices = [(cust['id'], f"{cust['first_name']} {cust['last_name']}") for cust in customers_data['results']] if customers_data else []

    customer = forms.ChoiceField(label='Покупатель')
    status = forms.ChoiceField(choices=[
        ('pending', 'В ожидании'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён')
    ], label='Статус')

class ReviewForm(forms.Form):
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        products_data = api_request('GET', 'products/', request) if request else None
        customers_data = api_request('GET', 'customers/', request) if request else None
        self.fields['product'].choices = [(prod['id'], prod['name']) for prod in products_data['results']] if products_data else []
        self.fields['customer'].choices = [(cust['id'], f"{cust['first_name']} {cust['last_name']}") for cust in customers_data['results']] if customers_data else []

    product = forms.ChoiceField(label='Товар')
    customer = forms.ChoiceField(label='Покупатель')
    rating = forms.IntegerField(min_value=1, max_value=5, label='Оценка')
    comment = forms.CharField(widget=forms.Textarea, label='Комментарий')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']