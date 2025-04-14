import pytest
from django.urls import reverse
from cart.models import Cart
from my_app.models import OrederModel
from django.shortcuts import get_object_or_404
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from decimal import Decimal

# Создаем фикстуры

@pytest.fixture
def dish_fixture():
    return OrederModel.objects.create(dish='Каша', price=25, quantity=4, total_price=100)


@pytest.fixture
def cart_fixture(dish_fixture):
    return Cart.objects.create(dish_name=dish_fixture, quantity=1)


# Тестируем функцию ---- def all_dishes(request):
@pytest.mark.django_db
def test_all_dishes(client):  # client отправляет запросы на сервер,
    # посредством методов get, post, put, delete и т.д. и получает от сервера response

    obj_1 = OrederModel.objects.create(dish='Салат', price=300, quantity=2, total_price=600)
    obj_2 = OrederModel.objects.create(dish='Газированная вода', price=100, quantity=3, total_price=300)

    url = reverse('cart:make_an_order')
    response = client.get(url)

    # Проверка статуса
    assert response.status_code == 200
    dishes = response.context['dishes_list']

    assert len(dishes) == 2

    assert 'Салат' in response.content.decode()
    assert 'Газированная вода' in response.content.decode()


@pytest.mark.django_db
def test_right_template(client):
    '''Тест на правильность выбора шаблона'''
    url = reverse('cart:make_an_order')
    response = client.get(url)

    assert 'cart_templates/dishes_list.html' in [a.name for a in response.templates]


# тестируем ---- def add_to_cart(request, id):
@pytest.mark.django_db
def test_add_to_cart(client, cart_fixture, dish_fixture):
    '''Тестирует add_to_cart'''
    choose_dish = get_object_or_404(OrederModel, id=dish_fixture.id)
    assert choose_dish.dish == 'Каша'

    # Тестировка отправки сообщения при ситуации когда блюдо в хранилище закончилось
    url = reverse('cart:add_to_cart', args=[dish_fixture.id])  # выбираем блюдо по id из хранилища и добавляем в корзину
    request = client.get(url)
    assert request.status_code == 302
    assert request.url == reverse('cart:make_an_order')

    dish_fixture.refresh_from_db()  # Обновлем базу данных
    cart_fixture.refresh_from_db()  # Обновлем базу данных
    assert dish_fixture.quantity == 3  # Функция отрабатывает и удаляет из хранилища 1 шт.
    assert cart_fixture.quantity == 2  # Функция отрабатывает и добавляе 1 шт.

    messages = list(get_messages(request.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Блюдо добавлено в корзину'

    with pytest.raises(ValidationError):
        cart_item = Cart.objects.create(dish_name=dish_fixture,
                                        quantity=0)  # При создании экземпляра корзины с 0 quantity б


@pytest.mark.django_db
def test_delete_from_cart(client):
    '''Тестируем код удаления из корзины и возврат обратно в хранилище'''

    oreder_item = OrederModel.objects.create(dish='Каша', price=25, quantity=4, total_price=100)
    cart_item = Cart.objects.create(dish_name=oreder_item, quantity=2)

    url = reverse('cart:delete_from_cart', args=[cart_item.id])
    request = client.get(url)

    assert request.url == reverse('cart:cart_list')  # Проверяем что редирект происходит на нужный путь
    assert request.status_code == 302  # Проверяем код ответа
    # Тесты добавления и удаленмия по 1 шт из бд
    oreder_item.refresh_from_db()  # Обновлем базу данных
    cart_item.refresh_from_db()  # Обновлем базу данных
    assert oreder_item.quantity == 5  # Добавляется количество в хранилище
    assert cart_item.quantity == 1  # Проверка на то что при вызове функции удаляется объект из корзины
    # Тесты сообщений
    messages = list(get_messages(request.wsgi_request))
    assert str(messages[0]) == 'Блюдо удалено из корзины'
    assert len(messages) == 1

    # Тест если quantity = 0, то объект не сохраняется
    cart_item.quantity = 0
    with pytest.raises(ValidationError):
        cart_item.save()

@pytest.mark.django_db
def test_delete_all(client):
    '''Проверяем полное удаление одной кнопкой'''

    oreder_item = OrederModel.objects.create(dish='Каша', price=25, quantity=4, total_price=100)
    cart_item = Cart.objects.create(dish_name=oreder_item, quantity=2)

    url = reverse('cart:delete_all', args=[cart_item.id])
    request = client.get(url)
    messages = list(get_messages(request.wsgi_request))

    assert request.status_code == 302 # Тест редиректа
    assert request.url == reverse('cart:cart_list') # Тест верного пути
    assert len(messages) == 1
    assert str(messages[0]) == 'Блюдо полностью удалено из вашего заказа'

    oreder_item.refresh_from_db()  #  Обновляем бд
    assert oreder_item.quantity == 6
    with pytest.raises(Cart.DoesNotExist):  # При попытке обновить бд вернется исключение это означает что объект не существует был удален
        cart_item.refresh_from_db()
        cart_item.save()

@pytest.mark.django_db
def test_cart_list(client):
    '''напишу потом'''

    obj_1 = OrederModel.objects.create(dish='Салат', price=300, quantity=2, total_price=600)
    obj_2 = OrederModel.objects.create(dish='Газированная вода', price=100, quantity=3, total_price=300)
    obj_cart_1 = Cart.objects.create(dish_name=obj_1, quantity=2)
    obj_cart_2 =  Cart.objects.create(dish_name=obj_2, quantity=5)

    url = reverse('cart:cart_list')
    request = client.get(url)
    assert request.status_code == 200

    # Проверяем что у нас в контекстах
    in_cart_context = request.context['in_cart']
    assert len(in_cart_context) == 2

    res_context = request.context['res']
    assert res_context == 7

    context_order_price = request.context['order_price']
    assert context_order_price == Decimal('1100.00')

    assert 'Салат' in request.content.decode()
    assert  'Газированная вода' in request.content.decode()
    assert '7' in request.content.decode()
    assert '1100' in request.content.decode()


