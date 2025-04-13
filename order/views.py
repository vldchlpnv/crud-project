from django.shortcuts import render, redirect
from .models import Order, OrderDish
from my_app.models import OrederModel
from cart.models import Cart
from django.db.models import Sum


def make_an_order(request):
    '''Представление для оформления заказа'''

    cart_items = Cart.objects.all()  # Вернет содержимое корзины
    if cart_items.exists(): #  Проверем на то что query не пустой
        create_order = Order.objects.create()

        # Перенесем объекты из корзины в таблицу OrderDish
        for cart_item in cart_items: # Переберет каждый обьект корзины
            OrderDish.objects.create(order_id=create_order.id, quantity=cart_item.quantity, dish_id=cart_item.dish_name_id )
    else:
        return redirect('cart:make_an_order') # После оформления заказа при обновлении страницы будет перенаправление в меню

    cart_items.delete()  # Очищаем корзину

    return render(request, 'order_template/order_done_template.html', {'create_order':create_order})
