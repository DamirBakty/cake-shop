import requests
from django.db.models.signals import pre_save
from django.dispatch import receiver
from cake.models import Advertising
from environs import Env

env = Env()
env.read_env()


@receiver(pre_save, sender=Advertising)
def pre_save_advertising(sender, instance, **kwargs):
    if not instance.pk:
        url = "https://t.ly/api/v1/link/shorten"
        headers = {
            "Authorization": f"Bearer {env.str('TLY_API_TOKEN')}"
        }
        payload = {
            "long_url": "http://www.ilovecake.ru/"
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        instance.url = response.json()["short_url"]
        instance.responses = 0
