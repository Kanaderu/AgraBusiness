from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserInfo, PaymentMethod


# Edit User Account Forms
class DjangoUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('user_type',)


# User Registration Forms
class RegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=UserInfo.USER_TYPE, help_text="User Account Type")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'user_type', 'username', 'password1', 'password2', )


# Payment Method Form associated with User
class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ('billing_address_line1', 'billing_address_line2', 'billing_zip_code', 'billing_state', 'billing_city', )
