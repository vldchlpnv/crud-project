# Generated by Django 5.1.7 on 2025-03-22 11:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrederModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.CharField(max_length=30, verbose_name='Блюдо')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(1, message='Количество не может быть 0')], verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Rjkbxtcndj должна быть положительным числом')], verbose_name='Цена')),
                ('total_price', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Общая стоимость должна быть положительным числом')], verbose_name='Стоимость заказа')),
            ],
            options={
                'verbose_name': 'Модель заказов',
            },
        ),
    ]
