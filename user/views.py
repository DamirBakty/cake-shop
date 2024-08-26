from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, reverse

from django.contrib import messages

from user.forms import RegistrationForm, UserProfileForm

User = get_user_model()


def register(request):
    if request.method == "POST":
        phone = request.POST.get('phone')

        try:
            user = User.objects.get(phone=phone)
            if user:
                login(request, user)
                return redirect(reverse('cake:index'))
        except User.DoesNotExist:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.phone
                user.set_unusable_password()
                user.save()

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect(reverse('cake:index'))
            else:
                messages.error(request, form.errors)

    return redirect(reverse('cake:index'))


def update_profile(request):
    if request.method == "POST":
        user = UserProfileForm(request.POST, instance=request.user)
        if user.is_valid():
            user.save()
        else:
            messages.error(request, user.errors)
        return redirect(reverse('cake:account'))
    return redirect(reverse('cake:account'))
