from django.urls import path

from user.views import register, update_profile

app_name = 'user'

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', update_profile, name='profile'),
]
