from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"autofocus": True}),
        max_length=150,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        strip=False,
    )
