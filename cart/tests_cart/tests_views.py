import pytest
from django.urls import reverse
from cart.models import Cart
from my_app.models import OrederModel

#def all_dishes(request):
#    '''Функция вернет все блюда которые еcть в наличии'''

#    dishes_list = OrederModel.objects.all()
#    return render(request, 'cart_templates/dishes_list.html', {'dishes_list': dishes_list})

@pytest.mark.django_db
def test_all_dishes(client): #  client отправляет запросы на сервер, посредством методов get, post, put, delete и т.д. и получает от сервера response

    obj_1 = OrederModel.objects.create(dish='Салат', price=300, quantity=2, total_price=600)
    obj_2 = OrederModel.objects.create(dish='Газированная вода', price=100, quantity=3, total_price=300)

    url = reverse('cart:make_an_order')
    response = client.get(url)

    # Проверка статуса
    assert response.status_code == 200
    dishes = response.context['dishes_list']
    print(dishes)
    assert len(dishes) == 2


    assert 'Салат' in response.content.decode()
    assert 'Газированная вода' in response.content.decode()

