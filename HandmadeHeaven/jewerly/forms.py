from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, Form, CharField, PasswordInput, EmailField, ValidationError

from .models import *


class RegisterForm(Form):
    username = CharField(max_length=150)
    password = CharField(widget=PasswordInput)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password')
        )
        custom_user = CustomUser.objects.create(
            user=user,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email')
        )
        return custom_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'
            field.label = field.label_tag(attrs={'class': 'form-label display-6 text-white mb-3'})


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3 '
            field.label = field.label_tag(attrs={'class': 'form-label display-6 text-white mb-3'})