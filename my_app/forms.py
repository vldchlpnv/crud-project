from django import forms


class MyForm(forms.Form):
    dish = forms.CharField(required=True, label='Наименование блюда', initial='Введите название блюда',
                           error_messages={'required': 'Поле не должно быть пустым'})
    quantity = forms.IntegerField(min_value=1, error_messages={'min_value': 'Количество не может быть отрицательным'},
                                  label='Количество', initial='Введите количество')
    price = forms.DecimalField(decimal_places=2, max_digits=8, error_messages={'min_value': 'Количество не может быть отрицательным'},
                                  label='Цена', initial='Введите цену')

    field_order = ['dish', 'price', 'quantity']