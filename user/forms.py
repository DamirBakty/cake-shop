from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'phone',
            'address',
            'email'
        )
