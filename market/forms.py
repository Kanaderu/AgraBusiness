from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.utils.translation import gettext as _


# Edit User Account Forms
class DjangoUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('user_type',)


# User Registration Forms
class RegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=UserInfo.USER_TYPE, help_text="User Account Type",
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=_("Enter the same password as above for verification."))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'user_type', 'username', 'password1', 'password2', )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'None'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Payment Method Form associated with User
class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ('billing_address_line1', 'billing_address_line2', 'billing_zip_code', 'billing_state', 'billing_city', )
        widgets = {
            'billing_address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_zip_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'billing_state': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_city': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ('name', 'number', 'ccv', 'exp')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'ccv': forms.NumberInput(attrs={'class': 'form-control'}),
            'exp': forms.DateInput(attrs={'class': 'form-control'}),
        }


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ('first_name', 'last_name', 'routing_number', 'account_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'routing_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'account_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }


CreditCardFormSet = forms.inlineformset_factory(PaymentMethod, CreditCard, form=CreditCardForm, extra=1)
BankAccountFormSet = forms.inlineformset_factory(PaymentMethod, BankAccount, form=BankAccountForm, extra=1)


# Cart Forms
class AddProduceItemToCart(forms.Form):
    quantity = forms.IntegerField(label=_('quantity'), min_value=0,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CartItem
