from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-имя")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_crud', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название производителя")
    country = models.CharField(max_length=100, verbose_name="Страна")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_crud')

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL-имя")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="Остаток на складе")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Производитель")
    main_image = models.ImageField(upload_to='products/', verbose_name="Основное изображение")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_crud', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('customer_crud', kwargs={'pk': self.id})

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Покупатель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=50, choices=[
        ('pending', 'В ожидании'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен')
    ], verbose_name="Статус")

    def __str__(self):
        return f"Заказ #{self.id}"

    def get_absolute_url(self):
        return reverse('order_crud', kwargs={'pk': self.id})

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Товар")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Покупатель")
    rating = models.PositiveIntegerField(verbose_name="Оценка")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв на {self.product.name} от {self.customer}"

    def get_absolute_url(self):
        return reverse('review_crud', kwargs={'pk': self.id})

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"