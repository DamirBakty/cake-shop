import uuid

import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from yookassa import Configuration, Payment

from cake.models import Cake, Order
from cake_shop.settings import YOOKASSA_ACCOUNT_ID, YOOKASSA_SECRET_KEY


def index(request):
    """Главная страница."""
    return render(request, 'cake/index.html')


def account(request):
    """Личный кабинет."""
    user = request.user
    orders = Order.objects.filter(user=user)
    history = Order.objects.filter(user=user, status='complete')
    context = {'user': user, 'orders': orders, 'history': history}
    return render(request, 'cake/lk.html', context)


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


def current_order(request):
    """Подтверждение текущего заказа."""
    cake_id = request.GET.get('cake_id', None)
    if cake_id:
        cake = Cake.objects.get(id=cake_id)
        inscription = None
        comment = None
    else:
        levels_number = request.POST.get('lvls')
        shape = request.POST.get('form')
        topping = request.POST.get('topping')
        berries = request.POST.get('berries')
        decor = request.POST.get('decor')
        inscription = request.POST.get('words')
        comment = request.POST.get('comment')
        cake = Cake.objects.create(
            levels_number=int(levels_number),
            shape=shape,
            topping=topping,
            berries=berries,
            decor=decor,
        )
    order = Order.objects.create(
        cake=cake,
        inscription=inscription,
        user=request.user,
        comment=comment,
        status='payment',
    )

    context = {
        'order': order,
    }
    return render(request, 'cake/current_order.html', context)


def payment(request):
    """Оплата заказа."""
    user = request.user
    user.username = request.POST.get('name')
    user.email = request.POST.get('email')
    user.address = request.POST.get('address')
    user.save()

    date = request.POST.get('date')
    time = request.POST.get('time')
    delivery_time = timezone.make_aware(
        datetime.datetime.strptime(
            date + time,
            "%Y-%m-%d%H:%M",
        ),
        timezone.get_current_timezone(),
    )

    fast_delivery = False
    if delivery_time - timezone.now() < datetime.timedelta(days=1):
        fast_delivery = True

    order = Order.objects.get(id=request.POST.get('order_id'))
    order.status = 'delivery'
    if not order.inscription:
        order.inscription = request.POST.get('words')
    order.courier_comment = request.POST.get('courier_comment')
    order.delivery_time = delivery_time
    order.fast_delivery = fast_delivery
    order.save()

    Configuration.account_id = YOOKASSA_ACCOUNT_ID
    Configuration.secret_key = YOOKASSA_SECRET_KEY
    payment = Payment.create({
        "amount": {
            "value": str(order.total_price),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://87.228.18.76:80/",
        },
        "capture": True,
        "description": "Оплата заказа"
    }, uuid.uuid4())

    return HttpResponseRedirect(payment.confirmation.confirmation_url)
