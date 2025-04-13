from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from my_app.models import OrederModel  # импорт модели блюд что есть в наличии
from .models import Cart  # импорт модели корзины
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import transaction


def all_dishes(request):
    '''Функция вернет все блюда которые еcть в наличии'''

    dishes_list = OrederModel.objects.all()
    return render(request, 'cart_templates/dishes_list.html', {'dishes_list': dishes_list})


def add_to_cart(request, id):
    '''Функция для добавление товаров в корзину'''

    #  блок выбора обьекта для добавления в корзину
    choose_dish = get_object_or_404(OrederModel, id=id)
    quantity_to_add = 1
    # Проверяем есть ли товар в хранилище если его нету то сразу вернется сообщение о его отсутсттвии при попытке добавить товар в корзину
    if choose_dish.quantity == 0:
        messages.error(request, 'Блюдо закончилось в хранилище')
        return redirect('cart:make_an_order')

    find_in_cart, created = Cart.objects.get_or_create(dish_name_id=id, defaults={'quantity': quantity_to_add})
    messages.success(request, 'Блюдо добавлено в корзину')  # Сообщение возвраащется после создания экземпляра класса

    if not created:
        find_in_cart.quantity += quantity_to_add
        find_in_cart.save()

    # примечание для себя: Что бы сообщения корректно работали(при редиректе) необходимо
    # прописывать код шаблона для сообщений в том шаблоне куда происходит редирект!
    # иначе сообщения не отобразятся
    # Блок удаление блюд из хранилища что бы уменьшать количество доступных блюд для заказа
    try:
        delete_from_order_model = OrederModel.objects.get(id=id)
        delete_from_order_model.quantity -= quantity_to_add
        delete_from_order_model.save()
    except Exception as e:
        print(f'Перехвачено исключение - {e}, количество товаров в хранилище не может быть меньше нуля')
    return redirect('cart:make_an_order')  # если задано пространство имен то его необходимо указывать в пути редиректа


def delete_from_cart(request, id):
    '''Представление которое удаляет блюдо из корзины
    и возвращает их обратно на склад'''

    get_for_delete = get_object_or_404(Cart, id=id)
    get_from_oreder_model = get_object_or_404(OrederModel,
                                              id=get_for_delete.dish_name_id)  # вернет вшений ключ который является id для таблицы OrederModel
    # Блок проеряет если количество больше нуля то удаляет по одному
    if get_for_delete.quantity > 1:
        get_for_delete.quantity -= 1
        messages.success(request, 'Блюдо удалено из корзины')

        get_from_oreder_model.quantity += 1  # прибавляем к количеству товаров в холодильнике +1
        get_from_oreder_model.save()  # сохраняем
        get_for_delete.save()
    # Если количество == 0, то позиция будет удалена из корзины
    else:
        get_for_delete.delete()  # Удаляем полностью позицию и
        get_from_oreder_model.quantity += 1  # Возвращаем удаленное в хранилище
        get_from_oreder_model.save()
        messages.success(request, 'Блюдо полностью удалено из вашего заказа')
    return redirect('cart:cart_list')


def delete_all(request, id):
    '''Удаляет за раз всю позицию в корзине'''
    get_for_delete = get_object_or_404(Cart, id=id)

    a = OrederModel.objects.get(id=get_for_delete.dish_name_id)  # Вернет экземпляр класса по id
    a.quantity += get_for_delete.quantity
    get_for_delete.delete()
    a.save()
    messages.success(request, 'Блюдо полностью удалено из вашего заказа')
    return redirect('cart:cart_list')


def cart_list(request):
    '''Вернет все блюда которые были добавлен в корзину'''
    in_cart = Cart.objects.all()
    res = Cart.objects.aggregate(total=Sum('quantity'))[
        'total']  # Вернет количество блюд в заказе. Ход с извлечением значения по ключу для того что бы возвращалось именно число а не ключ: значение
    obj = Cart.objects.values_list('dish_name_id', flat=True)  # тут находятся внешние ключи
    order_price = 0
    for i in obj:  # перебираем внешние ключи

        calc = OrederModel.objects.get(id=i).price * Cart.objects.get(dish_name_id=i).quantity
        order_price += calc

    return render(request, 'cart_templates/in_cart.html', {'in_cart': in_cart, 'res': res, 'order_price': order_price})
