from django.urls import path
from .views import my_view, create, edit, delete, main    # импорт представления


app_name = 'my_app'

urlpatterns = [path('', my_view, name='dish_form'),
               path('create/', create, name='create'),
               path('edit/<int:id>', edit, name='edit'),
               path('delete/<int:id>', delete, name='delete'),
               path('main/', main, name='main')]

