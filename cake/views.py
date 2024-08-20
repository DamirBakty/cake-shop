from django.shortcuts import render


def index(request):
    return render(request, 'cake/index.html')


def account(request):
    return render(request, 'cake/lk.html')


def orders(request):
    return render(request, 'cake/lk-order.html')
