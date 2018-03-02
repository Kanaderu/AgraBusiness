from django import forms
from django.contrib.auth.models import User
from .models import UserInfo


class DjangoUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('user_type', 'payment_method')

