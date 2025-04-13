from django.db import models
from uuid import uuid4
from my_app.models import OrederModel
from django.core.validators import MinValueValidator

class Order(models.Model):
    order_number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Номер заказа'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    dishes = models.ManyToManyField(
        OrederModel,
        through='OrderDish',
        related_name='orders',
        verbose_name='Блюда'
    )
    def save(self, *args, **kwargs):
        '''Генерирует уникальный номер заказа при сохранении'''
        if not self.order_number:
            self.order_number = str(uuid4())[:6].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Заказ № {self.order_number}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderDish(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    dish = models.ForeignKey(
        OrederModel,
        on_delete=models.CASCADE,
        verbose_name='Блюдо'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1, message='Количество должно быть положительным числом')]
    )# сюда положить количество блюд в позиции в заказе

    def total_price(self):
        '''Рассчитывает стоимость позиции в заказе'''
        return self.dish.price * self.quantity

    def __str__(self):
        return f'{self.order} - {self.dish.name} ({self.quantity})'

    class Meta:
        verbose_name = 'Блюдо в заказе'
        verbose_name_plural = 'Блюда в заказах'