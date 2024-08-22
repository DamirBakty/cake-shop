from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, reverse

from django.contrib import messages

from user.forms import RegistrationForm

User = get_user_model()


def register(request):
    if request.method == "POST":
        phone = request.POST.get('phone')

        try:
            existing_user = User.objects.get(phone=phone)
            user = authenticate(username=existing_user.username)
            if user:
                login(request, user)
                return redirect('some_view_name')
        except User.DoesNotExist:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.phone
                user.set_unusable_password()
                user.save()

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return  redirect(reverse('cake:index'))
            else:
                messages.error(request, form.errors)

    return redirect(reverse('cake:index'))
