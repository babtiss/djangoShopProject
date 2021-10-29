from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    image = models.ImageField(blank=True)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        ordering = ["category"]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    category = models.ForeignKey(Category, verbose_name='Категории', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name='Описание', null=True)
    image = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f"{self.title}, категория: {self.category.name}"

    def get_absolute_url(self):
        return reverse('products_detail', kwargs={'slug': self.slug})


class CartProduct(models.Model):
    class Meta:
        ordering = ["cart"]
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"

    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    owner = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.cart.owner}, {self.product.title}"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    class Meta:
        ordering = ["owner"]
        verbose_name = "Корзина"
        verbose_name_plural = "Все корзины"

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    number_of_products = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart {self.id},owner: {self.owner}"


class Customer(models.Model):
    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer')

    def __str__(self):
        return f"Покупатель {self.user.first_name, self.user.last_name}"


class Order(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'is_ready'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_READY, 'Новый зака'),
        (STATUS_COMPLETED, 'Новый зака'),
        (STATUS_IN_PROGRESS, 'Новый зака'),
    )
    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'
    BUYING_CHOICES = (
        (BUYING_TYPE_SELF, 'самовывоз'),
        (BUYING_TYPE_DELIVERY, 'доставка'),
    )
    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orderer',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя', default='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', default='Фамилия')
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=100, verbose_name='Тип заказа', choices=BUYING_CHOICES,
                                   default=BUYING_TYPE_SELF)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.id}, {self.cart}'
