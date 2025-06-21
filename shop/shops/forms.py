from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .utils import api_request

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название')
    slug = forms.SlugField(max_length=100, required=False, label='Slug')
    image = forms.ImageField(required=False, label='Изображение')

class ManufacturerForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название')
    country = forms.CharField(max_length=100, label='Страна')

class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название')
    slug = forms.SlugField(max_length=100, required=False, label='Slug')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')
    price = forms.DecimalField(max_digits=10, decimal_places=2, label='Цена')
    stock = forms.IntegerField(label='Остаток')
    category = forms.ChoiceField(label='Категория')
    manufacturer = forms.ChoiceField(required=False, label='Производитель')
    main_image = forms.ImageField(required=False, label='Изображение')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            categories_data = api_request('GET', 'categories/', request)
            self.fields['category'].choices = [(str(cat['id']), cat['name']) for cat in categories_data.get('results', [])] if categories_data else []
            manufacturers_data = api_request('GET', 'manufacturers/', request)
            self.fields['manufacturer'].choices = [('', '---------')] + [(str(m['id']), m['name']) for m in manufacturers_data.get('results', [])] if manufacturers_data else [('', '---------')]
        else:
            self.fields['category'].choices = []
            self.fields['manufacturer'].choices = [('', '---------')]

class CustomerForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, required=False, label='Телефон')

class OrderForm(forms.Form):
    customer = forms.ChoiceField(label='Покупатель')
    status = forms.ChoiceField(choices=[
        ('pending', 'В ожидании'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён')
    ], label='Статус')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            customers_data = api_request('GET', 'customers/', request)
            self.fields['customer'].choices = [(str(cust['id']), f"{cust['first_name']} {cust['last_name']}") for cust in customers_data.get('results', [])] if customers_data else []
        else:
            self.fields['customer'].choices = []

class ReviewForm(forms.Form):
    product = forms.ChoiceField(label='Товар')
    customer = forms.ChoiceField(label='Покупатель')
    rating = forms.IntegerField(min_value=1, max_value=5, label='Оценка')
    comment = forms.CharField(widget=forms.Textarea, label='Комментарий')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            products_data = api_request('GET', 'products/', request)
            self.fields['product'].choices = [(str(prod['id']), prod['name']) for prod in products_data.get('results', [])] if products_data else []
            customers_data = api_request('GET', 'customers/', request)
            self.fields['customer'].choices = [(str(cust['id']), f"{cust['first_name']} {cust['last_name']}") for cust in customers_data.get('results', [])] if customers_data else []
        else:
            self.fields['product'].choices = []
            self.fields['customer'].choices = []