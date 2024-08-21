from django.shortcuts import render

from cake.models import Cake


def index(request):
    return render(request, 'cake/index.html')


def account(request):
    return render(request, 'cake/lk.html')


def orders(request):
    return render(request, 'cake/lk-order.html')


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
