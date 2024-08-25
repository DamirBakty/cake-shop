from django.contrib import admin

import requests
from environs import Env

from .models import Advertising, Cake, Order


env = Env()
env.read_env()


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    readonly_fields = ('price',)
    list_filter = ('is_base',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'cake', 'get_address', 'get_phone', 'status')
    readonly_fields = (
        'total_price',
        'created_date',
        'fast_delivery',
    )


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ('url', 'text', 'responses',)
    readonly_fields = ('url', 'responses',)

    def changelist_view(self, request, extra_context=None):
        advertising = Advertising.objects.all()
        headers = {
            "Authorization": f"Bearer {env.str('TLY_API_TOKEN')}"
        }
        url = "https://t.ly/api/v1/link/stats"
        for ad in advertising:
            params = {"short_url": ad.url}
            response = requests.get(url,
                                    headers=headers,
                                    params=params)
            response.raise_for_status()
            ad.responses = response.json()["clicks"]
        Advertising.objects.bulk_update(advertising, ['responses'])
        return super().changelist_view(request, extra_context=extra_context)
