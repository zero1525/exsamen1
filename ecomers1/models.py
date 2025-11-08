from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name=models.CharField(verbose_name="имя", max_length=50)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f'{self.id} - {self.name}'


class Brand(models.Model):
    name=models.CharField(verbose_name="имя", max_length=50)

    class Meta:
        verbose_name = "Брэнд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return f'{self.id} - {self.name}'

class Goods (models.Model):
    name=models.CharField(verbose_name="имя", max_length=50)
    description=models.TextField(verbose_name='описание', max_length=500)
    price=MoneyField(verbose_name="цена", max_digits=14, decimal_places=2, default_currency='USD')
    img=models.ImageField( blank=True, null=True, verbose_name="Изоброжения")
    category=models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="категория")
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="бренд")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f'{self.id} - {self.name}-{self.price}'


class Basket (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    goods=models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="товар")
    quantity=models.PositiveIntegerField(verbose_name="количество", default=0)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f'{self.quantity}'
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)