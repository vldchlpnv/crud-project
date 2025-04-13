from django.db import models
from my_app.models import OrederModel
from django.core.exceptions import ValidationError


class Cart(models.Model):
    '''Модель корзины'''

    dish_name = models.ForeignKey(OrederModel, on_delete=models.CASCADE, verbose_name='Блюдо', unique=True)  #
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def position_total_price(self):
        '''Вернет общую стоимость позиции в корзине'''

        return self.dish_name.price * self.quantity

    def clean(self):
        '''Првоерка на то что
        quantity не может быть == 0'''
        if self.quantity == 0:
            raise ValidationError('Количество не может быть равным 0')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Корзина'
