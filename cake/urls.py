from django.urls import path

from cake.views import get_catalog, index, account, orders

app_name = 'cake'
urlpatterns = [
    path('', index, name='index'),
    path('account/', account, name='account'),
    path('orders/', orders, name='orders'),
    path('catalog/', get_catalog, name='catalog'),
    path('catalog/<slug:slug>/', get_catalog, name='catalog_reason'),
]
