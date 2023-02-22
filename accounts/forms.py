from django import forms
from django.contrib.auth.forms import UserCreationForm


from .models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Введите ваш email'
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
