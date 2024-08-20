from django.urls import path

from cake.views import index, account, orders

app_name = 'cake'
urlpatterns = [
    path('', index, name='index'),
    path('account', account, name='account'),
    path('orders', orders, name='orders'),
]
