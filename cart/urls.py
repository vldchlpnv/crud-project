from django.urls import path, include
from .views import all_dishes, add_to_cart, cart_list, delete_from_cart, delete_all
app_name = 'cart'

urlpatterns=[path('make_an_order/', all_dishes, name='make_an_order'),
             path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
             path('cart_list/', cart_list, name='cart_list'),
             path('delete_from_cart/<int:id>/', delete_from_cart, name='delete_from_cart'),
             path('delete_all/<int:id>/', delete_all, name='delete_all'),
             ]