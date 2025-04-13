from django.urls import path
from .views import make_an_order



app_name = 'order'

urlpatterns = [path('plase_an_order/', make_an_order, name ='plase_an_order'),
               ]