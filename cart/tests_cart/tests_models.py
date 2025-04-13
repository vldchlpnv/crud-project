import pytest
from cart.models import Cart
from my_app.models import OrederModel
from django.core.exceptions import ValidationError, ObjectDoesNotExist


@pytest.fixture()
def cart_fixture():
    '''Фикстура для создания экземпляра класса OrederModel,
    т.к. корзина связана с ней внещним ключом'''
    # Создаем и возвращаем экземпляр класса OrederModel
    return OrederModel.objects.create(dish='Манты', price=100, quantity=3, total_price=300)


@pytest.mark.django_db  # Декоратор для доступа к базе данных(используется там где происходит работа с бд)
def test_cart_model(cart_fixture):
    '''Тест проверяет создание объекта Cart и корректность полей'''
    cart_item = Cart.objects.create(dish_name=cart_fixture, quantity=6)

    assert cart_item.quantity == 6
    assert cart_item.dish_name_id == cart_fixture.id


@pytest.mark.django_db
def test_position_total_price(cart_fixture):
    '''Тест проверяет расчет общей стоимости позиции в корзине'''

    cart_item = Cart.objects.create(dish_name=cart_fixture, quantity=6)

    assert cart_fixture.price * cart_item.quantity == 600


@pytest.mark.django_db
def test_change_price(cart_fixture):
    '''Тест на изменение общей стоимости позиции в корзине
    при изменении цены в OrederModel'''
    cart_item = Cart.objects.create(dish_name=cart_fixture, quantity=6)  # Создаем экземпляр в корзине
    cart_fixture.price = 300  # Изменяем цену позиции
    cart_fixture.save()
    assert cart_fixture.price * cart_item.quantity == cart_item.position_total_price()


@pytest.mark.django_db
def test_cart_quantity_validation(cart_fixture):
    '''Тест на правильность валидации'''
    with pytest.raises(ValidationError):  # Данная конструкция проверить выбросит ли код ниже искючение.
        # Т.К. в модели есть методы в соответствии с которыми исключение должно быть выброшено
        cart_item = Cart.objects.create(dish_name=cart_fixture, quantity=-6)
        cart_item.save()
        # То же самое и тут
    with pytest.raises(ValidationError):
        cart_item = Cart.objects.create(dish_name=cart_fixture, quantity=0)
        cart_item.save()


@pytest.mark.django_db
def test_cascated_delete(cart_fixture):
    '''Тест на каскадное
     удаление экземпляра в корзине'''
    cart_item = Cart.objects.create(dish_name=cart_fixture, quantity=6)
    cart_fixture.delete()

    with pytest.raises(Cart.DoesNotExist):
        cart = Cart.objects.get(id=cart_item.id)


@pytest.mark.django_db
def test_connected_obect():
    '''Поведение Cart, при отсутствии OrederModel'''

    with pytest.raises(ValidationError):
        Cart.objects.create(dish_name_id=666, quantity=666)


@pytest.mark.django_db
def test_unique_items(cart_fixture):  # Что бы тест проходил поле dish_name должно быть unique=True
    '''Тест на уникальность полей, не создастся 2 одинаковых поля,
     любое блюдо которое мы добавим если оно уже есть в корзине
     только увеличит количество позиции в корзине'''
    cart_item = Cart.objects.create(dish_name=cart_fixture, quantity=2)
    with pytest.raises(Exception):
        Cart.objects.create(dish_name=cart_fixture, quantity=2)


@pytest.mark.django_db
def test_empty_cart(cart_fixture):
    '''Тест на попытку обратиться к пустой корзине'''
    create_obj = Cart.objects.create(dish_name=cart_fixture, quantity=2)
    obj_id = create_obj.id
    create_obj.delete()
    with pytest.raises(Cart.DoesNotExist):
        obj = Cart.objects.get(id=obj_id)

@pytest.mark.django_db
def test_update_cart(cart_fixture):
    '''Тест на корректность обновления'''
    cart_item = Cart.objects.create(dish_name=cart_fixture, quantity=2)
    cart_item.quantity += 2
    cart_item.save()
    assert cart_item.quantity == 4



