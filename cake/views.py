import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from environs import Env
from yookassa import Configuration, Payment

from cake.models import Cake, Order

env = Env()
env.read_env()


def index(request):
    return render(request, 'cake/index.html')


def account(request):
    return render(request, 'cake/lk.html')


def orders(request):
    user = request.user
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=user)
        context = {'user': user, 'orders': orders}
        return render(request, 'cake/lk-order.html', context)
    return render(request, 'registration/template.html')


def get_catalog(request, slug=None):
    """Вывод каталога."""
    REASONS = {
        'tea': 'На чаепитие',
        'birthday': 'На день рождения',
        'wedding': 'На свадьбу',
    }
    base_cakes = Cake.objects.filter(is_base=True)
    if slug:
        cakes = base_cakes.filter(reason=slug)
    else:
        cakes = base_cakes
    title = REASONS.get(slug)
    context = {'cakes': cakes, 'title': title}
    return render(request, 'cake/catalog.html', context)


def payment(request):
    """Оплата заказа."""
    Configuration.account_id = env.int('YOOKASSA_ACCOUNT_ID')
    Configuration.secret_key = env.str('YOOKASSA_SECRET_KEY')

    payment = Payment.create({
        "amount": {
            "value": "100",  # str(order.total_price)
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000/",
        },
        "capture": True,
        "description": "Оплата заказа"
    }, uuid.uuid4())

    return HttpResponseRedirect(payment.confirmation.confirmation_url)
