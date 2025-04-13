import pytest
from django.urls import reverse
from cart.models import Cart
from my_app.models import OrederModel
from django.shortcuts import get_object_or_404
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
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
    url = reverse('cart:add_to_cart', args=[dish_fixture.id]) # выбираем блюдо по id из хранилища и добавляем в корзину
    request = client.get(url)
    assert request.status_code == 302
    assert request.url == reverse('cart:make_an_order')


    dish_fixture.refresh_from_db()  # Обновлем базу данных
    cart_fixture.refresh_from_db()  # Обновлем базу данных
    print(dish_fixture.quantity)
    assert dish_fixture.quantity == 3  # Функция отрабатывает и удаляет из хранилища 1 шт.
    assert cart_fixture.quantity == 2  # Функция отрабатывает и добавляе 1 шт.

    messages = list(get_messages(request.wsgi_request))

    assert len(messages) == 1
    assert str(messages[0]) == 'Блюдо добавлено в корзину'

    with pytest.raises(ValidationError):
        cart_item = Cart.objects.create(dish_name=dish_fixture, quantity=0)  #При создании экземпляра корзины с 0 quantity б
                                                                             #Будет выброшено исключение
















