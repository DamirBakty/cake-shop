import datetime
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


EXTRA_PRICES = {
    'levels': {'1': 400, '2': 750, '3': 1100, },
    'shapes': {'square': 600, 'circle': 400, 'rectangle': 1000, },
    'toppings': {
        'no_topping': 0,
        'white_sauce': 200,
        'caramel_syrup': 180,
        'maple_syrup': 200,
        'strawberry_syrup': 300,
        'blueberry_syrup': 350,
        'milk_chocolate': 200,
    },
    'berries': {
        'no_berries': 0,
        'blackberry': 400,
        'raspberry': 300,
        'blueberry': 450,
        'strawberry': 500,
    },
    'decor': {
        'no_decor': 0,
        'pistachio': 300,
        'meringue': 400,
        'hazelnut': 350,
        'pecan': 300,
        'marshmallow': 200,
        'marzipan': 280,
    },
    'inscription': 500,
    'express_coefficient': 1.2,
}

User = get_user_model()


class CakeQuerySet(models.QuerySet):
    """Пользовательский класс QuerySet для модели Cake."""
    def get_price(self):
        """Вычислить и записать стоимость торта."""
        cake = self.first()
        price = (
            EXTRA_PRICES['levels'][str(cake.levels_number)] +
            EXTRA_PRICES['shapes'][cake.shape] +
            EXTRA_PRICES['toppings'][cake.topping] +
            EXTRA_PRICES['berries'][cake.berries] +
            EXTRA_PRICES['decor'][cake.decor]
        )
        self.update(price=price)


class Cake(models.Model):
    """Модель торта, собранного самостоятельно."""
    LEVEL_CHOICES = [(1, '1 уровень'), (2, '2 уровня'), (3, '3 уровня'),]
    SHAPE_CHOICES = [
        ('square', 'квадрат'),
        ('circle', 'круг'),
        ('rectangle', 'прямоугольник'),
    ]
    TOPPING_CHOICES = [
        ('no_topping', 'без топпинга'),
        ('white_sauce', 'белый соус'),
        ('caramel_syrup', 'карамельный сироп'),
        ('maple_syrup', 'кленовый сироп'),
        ('strawberry_syrup', 'клубничный сироп'),
        ('blueberry_syrup', 'черничный сироп'),
        ('milk_chocolate', 'молочный шоколад'),
    ]
    BERRIES_CHOICES = [
        ('no_berries', 'без ягод'),
        ('blackberry', 'ежевика'),
        ('raspberries', 'малина'),
        ('blueberry', 'голубика'),
        ('strawberry', 'клубника'),
    ]
    DECOR_CHOICES = [
        ('no_decor', 'без декора'),
        ('pistachio', 'фисташки'),
        ('meringue', 'безе'),
        ('hazelnut', 'фундук'),
        ('pecan', 'пекан'),
        ('marshmallow', 'маршмеллоу'),
        ('marzipan', 'марципан'),
    ]
    REASONS = [
        ('tea', 'На чаепитие'),
        ('birthday', 'На день рождения'),
        ('wedding', 'На свадьбу'),
    ]
    title = models.CharField(
        'Название',
        max_length=100,
        default='Пользовательский торт',
    )
    levels_number = models.SmallIntegerField(
        'Количество уровней',
        choices=LEVEL_CHOICES,
    )
    shape = models.CharField(
        'Форма',
        max_length=50,
        choices=SHAPE_CHOICES,
        )
    topping = models.CharField(
        'Топпинг',
        max_length=50,
        choices=TOPPING_CHOICES,
    )
    berries = models.CharField(
        'Ягоды',
        max_length=50,
        choices=BERRIES_CHOICES,
        blank=True,
        null=True,
    )
    decor = models.CharField(
        'Декор',
        max_length=50,
        choices=DECOR_CHOICES,
        blank=True,
        null=True,
    )
    price = models.IntegerField('Цена', blank=True, null=True)
    is_base = models.BooleanField('Стандартный торт', default=False)
    photo = models.ImageField(
        upload_to='cakes/',
        verbose_name='Фото',
        default='../static/cake/img/default_cake.png',
    )
    reason = models.CharField(
        'Причина',
        max_length=50,
        choices=REASONS,
        blank=True,
        null=True,
    )
    objects = CakeQuerySet.as_manager()

    class Meta:
        verbose_name = 'Торт'
        verbose_name_plural = 'Торты'

    def __str__(self):
        if self.title == 'Пользовательский торт':
            return f'{self.title} {self.id}'
        return self.title

    def save(self, *args, **kwargs):
        """Вычислить и записать стоимость торта при сохранении."""
        price = (
            EXTRA_PRICES['levels'][str(self.levels_number)] +
            EXTRA_PRICES['shapes'][self.shape] +
            EXTRA_PRICES['toppings'][self.topping] +
            EXTRA_PRICES['berries'].get(self.berries, 0) +
            EXTRA_PRICES['decor'].get(self.decor, 0)
        )
        self.price = price
        super(Cake, self).save()


class OrderQuerySet(models.QuerySet):
    """Пользовательский класс QuerySet для модели Order."""
    def is_fast_delivery(self):
        """Определить, что доставка срочная"""
        if self.delivery_time - self.created_date < datetime.timedelta(days=1):
            return True


class Order(models.Model):
    """Модель заказа."""
    STATUSES = [
        ('payment', 'В оплате'),
        ('delivery', 'В доставке'),
        ('complete', 'Завершен'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь',
    )
    comment = models.TextField('Комментарий', blank=True, null=True,)
    courier_comment = models.TextField(
        'Комментарий курьеру',
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(
        'Дата создания заказа',
        auto_now_add=True,
    )
    delivery_time = models.DateTimeField(
        'Время доставки',
        blank=True,
        null=True,
    )
    cake = models.ForeignKey(
        Cake,
        verbose_name='Торт',
        related_name='orders',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    inscription = models.CharField(
        'Надпись',
        max_length=200,
        blank=True,
        null=True,
    )
    total_price = models.FloatField('Конечная цена', blank=True, null=True)
    fast_delivery = models.BooleanField('Быстрая доставка', default=False)
    status = models.CharField(
        'Статус заказа',
        max_length=50,
        choices=STATUSES,
        blank=False,
        null=False,
        default='payment',
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ клиента {self.user.username} {self.user.phone}'

    def get_total_price(self):
        """Вычислить и записать стоимость заказа."""
        total_price = self.cake.price
        if self.inscription:
            total_price += EXTRA_PRICES['inscription']
        if self.fast_delivery:
            total_price *= EXTRA_PRICES['express_coefficient']
        self.update(total_price=total_price)

    def clean(self):
        """Для выведения ошибки в админке"""
        if (self.delivery_time and self.created_date and self.delivery_time
                < self.created_date):
            raise ValidationError('Неверная дата доставки')

    def save(self, *args, **kwargs):
        """
        Получить стоимость заказа и дату доставки при сохранении.
        Определение статуса срочной доставки.
        """
        total_price = self.cake.price
        if self.inscription:
            total_price += EXTRA_PRICES['inscription']
        if self.fast_delivery:
            total_price *= EXTRA_PRICES['express_coefficient']
        self.total_price = total_price

        if not self.delivery_time:
            self.created_date = timezone.now()
            self.delivery_time = self.created_date + datetime.timedelta(days=2)
        if self.delivery_time < self.created_date:
            return super(Order, self).clean()

        if self.delivery_time - self.created_date < datetime.timedelta(days=1):
            self.fast_delivery = True

        super(Order, self).save()

    @admin.display(description='Адрес')
    def get_address(self):
        return self.user.address

    @admin.display(description='Номер телефона')
    def get_phone(self):
        return self.user.phone


class Advertising(models.Model):
    """Модель рекламы."""
    url = models.URLField('Ссылка', blank=True)
    text = models.TextField('Текст рекламы')
    responses = models.IntegerField(
        'Количество откликов',
        null=True,
        blank=True,
        default=0,
    )

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Реклама'
