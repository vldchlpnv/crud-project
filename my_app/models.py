from django.db import models
from django.core.validators import MinValueValidator

class OrederModel(models.Model):

    dish = models.CharField(max_length=30, verbose_name='Блюдо')
    price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена', validators=[MinValueValidator(1, message='Цена не может быть 0')])
    quantity = models.PositiveIntegerField(verbose_name='Количество', validators=[MinValueValidator(1, message='Количество должно быть положительным числом')])
    total_price = models.PositiveIntegerField(verbose_name='Стоимость заказа', validators=[MinValueValidator(1, message='Общая стоимость должна быть положительным числом')], null=True)

    class Meta:
        verbose_name = 'Модель заказов'

    def total_price_counter(self):
        self.total_price = self.price * self.quantity
        return self.total_price

    def save(self, *args, **kwargs):
        self.total_price = self.total_price_counter()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.dish} x {self.quantity} = {self.total_price}'

