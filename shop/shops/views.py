from django.views.generic import View, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Category, Product, Customer, Order, Review, Manufacturer
from .forms import CategoryForm, ProductForm, CustomerForm, OrderForm, ReviewForm, ManufacturerForm

class AdminMenuView(View):
    template_name = 'admin_menu.html'

    def get(self, request):
        return render(request, self.template_name)

class CategoryCRUDView(View):
    template_name = 'category_crud.html'

    def get(self, request, slug=None):
        categories = Category.objects.all()
        form = CategoryForm()
        edit_category = None
        if slug:
            edit_category = get_object_or_404(Category, slug=slug)
            form = CategoryForm(instance=edit_category)
        return render(request, self.template_name, {
            'categories': categories,
            'form': form,
            'edit_category': edit_category,
            'request': request,
        })

    def post(self, request, slug=None):
        if 'delete' in request.POST:
            category = get_object_or_404(Category, slug=request.POST['slug'])
            category.delete()
            messages.success(request, 'Категория удалена.')
            return redirect('category_crud')
        
        form = CategoryForm(request.POST, instance=get_object_or_404(Category, slug=slug) if slug else None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория сохранена.')
            return redirect('category_crud')
        categories = Category.objects.all()
        return render(request, self.template_name, {
            'categories': categories,
            'form': form,
            'edit_category': get_object_or_404(Category, slug=slug) if slug else None,
            'request': request,
        })

class ProductCRUDView(View):
    template_name = 'product_crud.html'

    def get(self, request, slug=None, manufacturer_id=None):
        products = Product.objects.all()
        manufacturers = Manufacturer.objects.all()
        product_form = ProductForm()
        manufacturer_form = ManufacturerForm()
        edit_product = None
        edit_manufacturer = None

        if slug:
            edit_product = get_object_or_404(Product, slug=slug)
            product_form = ProductForm(instance=edit_product)
        if manufacturer_id:
            edit_manufacturer = get_object_or_404(Manufacturer, id=manufacturer_id)
            manufacturer_form = ManufacturerForm(instance=edit_manufacturer)

        return render(request, self.template_name, {
            'products': products,
            'manufacturers': manufacturers,
            'product_form': product_form,
            'manufacturer_form': manufacturer_form,
            'edit_product': edit_product,
            'edit_manufacturer': edit_manufacturer,
            'request': request,
        })

    def post(self, request, slug=None, manufacturer_id=None):
        products = Product.objects.all()
        manufacturers = Manufacturer.objects.all()

        if 'delete_product' in request.POST:
            product = get_object_or_404(Product, slug=request.POST['slug'])
            product.delete()
            messages.success(request, 'Товар удален.')
            return redirect('product_crud')
        
        if 'delete_manufacturer' in request.POST:
            manufacturer = get_object_or_404(Manufacturer, id=request.POST['manufacturer_id'])
            manufacturer.delete()
            messages.success(request, 'Производитель удален.')
            return redirect('product_crud')

        if 'save_product' in request.POST:
            product_form = ProductForm(request.POST, instance=get_object_or_404(Product, slug=slug) if slug else None)
            if product_form.is_valid():
                product_form.save()
                messages.success(request, 'Товар сохранен.')
                return redirect('product_crud')
            else:
                messages.error(request, 'Ошибка в форме товара.')
                manufacturer_form = ManufacturerForm()
                return render(request, self.template_name, {
                    'products': products,
                    'manufacturers': manufacturers,
                    'product_form': product_form,
                    'manufacturer_form': manufacturer_form,
                    'edit_product': get_object_or_404(Product, slug=slug) if slug else None,
                    'edit_manufacturer': None,
                    'request': request,
                })

        if 'save_manufacturer' in request.POST:
            manufacturer_form = ManufacturerForm(request.POST, instance=get_object_or_404(Manufacturer, id=manufacturer_id) if manufacturer_id else None)
            if manufacturer_form.is_valid():
                manufacturer_form.save()
                messages.success(request, 'Производитель сохранен.')
                return redirect('product_crud')
            else:
                messages.error(request, 'Ошибка в форме производителя.')
                product_form = ProductForm()
                return render(request, self.template_name, {
                    'products': products,
                    'manufacturers': manufacturers,
                    'product_form': product_form,
                    'manufacturer_form': manufacturer_form,
                    'edit_product': None,
                    'edit_manufacturer': get_object_or_404(Manufacturer, id=manufacturer_id) if manufacturer_id else None,
                    'request': request,
                })

        # Fallback in case of unexpected POST
        return render(request, self.template_name, {
            'products': products,
            'manufacturers': manufacturers,
            'product_form': ProductForm(),
            'manufacturer_form': ManufacturerForm(),
            'edit_product': None,
            'edit_manufacturer': None,
            'request': request,
        })

class CustomerCRUDView(View):
    template_name = 'customer_crud.html'

    def get(self, request, pk=None):
        customers = Customer.objects.all()
        form = CustomerForm()
        edit_customer = None
        if pk:
            edit_customer = get_object_or_404(Customer, pk=pk)
            form = CustomerForm(instance=edit_customer)
        return render(request, self.template_name, {
            'customers': customers,
            'form': form,
            'edit_customer': edit_customer,
            'request': request,
        })

    def post(self, request, pk=None):
        if 'delete' in request.POST:
            customer = get_object_or_404(Customer, pk=request.POST['pk'])
            customer.delete()
            messages.success(request, 'Покупатель удален.')
            return redirect('customer_crud')
        
        form = CustomerForm(request.POST, instance=get_object_or_404(Customer, pk=pk) if pk else None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Покупатель сохранен.')
            return redirect('customer_crud')
        customers = Customer.objects.all()
        return render(request, self.template_name, {
            'customers': customers,
            'form': form,
            'edit_customer': get_object_or_404(Customer, pk=pk) if pk else None,
            'request': request,
        })

class OrderCRUDView(View):
    template_name = 'order_crud.html'

    def get(self, request, pk=None):
        orders = Order.objects.all()
        form = OrderForm()
        edit_order = None
        if pk:
            edit_order = get_object_or_404(Order, pk=pk)
            form = OrderForm(instance=edit_order)
        return render(request, self.template_name, {
            'orders': orders,
            'form': form,
            'edit_order': edit_order,
            'request': request,
        })

    def post(self, request, pk=None):
        if 'delete' in request.POST:
            order = get_object_or_404(Order, pk=request.POST['pk'])
            order.delete()
            messages.success(request, 'Заказ удален.')
            return redirect('order_crud')
        
        form = OrderForm(request.POST, instance=get_object_or_404(Order, pk=pk) if pk else None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ сохранен.')
            return redirect('order_crud')
        orders = Order.objects.all()
        return render(request, self.template_name, {
            'orders': orders,
            'form': form,
            'edit_order': get_object_or_404(Order, pk=pk) if pk else None,
            'request': request,
        })

class ReviewCRUDView(View):
    template_name = 'review_crud.html'

    def get(self, request, pk=None):
        reviews = Review.objects.all()
        form = ReviewForm()
        edit_review = None
        if pk:
            edit_review = get_object_or_404(Review, pk=pk)
            form = ReviewForm(instance=edit_review)
        return render(request, self.template_name, {
            'reviews': reviews,
            'form': form,
            'edit_review': edit_review,
            'request': request,
        })

    def post(self, request, pk=None):
        if 'delete' in request.POST:
            review = get_object_or_404(Review, pk=request.POST['pk'])
            review.delete()
            messages.success(request, 'Отзыв удален.')
            return redirect('review_crud')
        
        form = ReviewForm(request.POST, instance=get_object_or_404(Review, pk=pk) if pk else None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв сохранен.')
            return redirect('review_crud')
        reviews = Review.objects.all()
        return render(request, self.template_name, {
            'reviews': reviews,
            'form': form,
            'edit_review': get_object_or_404(Review, pk=pk) if pk else None,
            'request': request,
        })

class AllProductsView(ListView):
    template_name = 'all_products.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context

def home(request):
    # Получаем три самых популярных товара по количеству в наличии
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
    return render(request, 'categories.html', {'request': request})

def all_products(request):
    return render(request, 'all_products.html', {'request': request})

def cart(request):
    return render(request, 'cart.html', {'request': request})