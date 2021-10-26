from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AccountForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length=100, required=False)
    phone = forms.CharField(max_length=12, required=False)
    address = forms.CharField(max_length=500, required=False)
    image = forms.FileField(required=False)
