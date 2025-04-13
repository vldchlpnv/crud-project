from django.shortcuts import render
from .forms import MyForm
from django.http import HttpResponse, HttpResponseRedirect
from decimal import Decimal
from .models import OrederModel
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

def main(request):

    return render(request, 'base.html')

def my_view(request):
    '''Вернет все блюда из базы данных'''
    all_dishes = OrederModel.objects.all()
    return render(request, 'my_app_template/form_template.html', {'all_dishes': all_dishes})


def create(request):
    '''Сохранение в бд'''
    if request.method == 'POST':

        dish = request.POST.get('dish')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        try:
            price = int(price)
            quantity = int(quantity)

            oreder_model, created = OrederModel.objects.get_or_create(dish=dish, price=price,
                                                                      defaults={'quantity': quantity})
            if not created:
                # Если объект уже существует, увеличиваем количество
                oreder_model.quantity += quantity
                oreder_model.save()

        except ValueError:
            # Обработка ошибок при преобразовании данных
            return render(request, 'error.html',
                          {'message': 'Некорректные данные. Пожалуйста, введите числовые значения.'})

        return HttpResponseRedirect('/')


def edit(request, id):
    '''Редактируем запись'''
    order_model = get_object_or_404(OrederModel, id=id)
    if request.method == 'POST':
        # order_model = OrederModel() если тут создавать новый экземпляр класса то тогда данные будут добавляться, а не обновляться

        order_model.dish = request.POST.get('dish')
        order_model.price = request.POST.get('price')
        order_model.quantity = request.POST.get('quantity')

        if order_model.dish and order_model.price and order_model.quantity:
            order_model.price = int(order_model.price)
            order_model.quantity = int(order_model.quantity)
            order_model.save()
            return HttpResponseRedirect('/')
    else:

        return render(request, 'my_app_template/edit.html', {'order_model': order_model})


def delete(request, id):
    '''Удаление записи из базы данных'''
    order_model = get_object_or_404(OrederModel, id=id)
    # if request.method == 'POST':
    order_model.delete()
    return HttpResponseRedirect('/')
