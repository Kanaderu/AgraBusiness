from django.shortcuts import get_object_or_404, render
from .forms import DjangoUserForm, UserInfoForm, RegisterForm, PaymentMethodForm, CreditCardFormSet, BankAccountFormSet
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView, CreateView
from .models import CreditCard, PaymentMethod


# Edit User Views
class EditUserView(View):
    user_form = DjangoUserForm
    userinfo_form = UserInfoForm
    pmethod_form = PaymentMethodForm
    template_name = 'user.html'

    decorators = [transaction.atomic, login_required]

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        user_form = self.user_form(instance=request.user)
        userinfo_form = self.userinfo_form(instance=request.user.userinfo)
        pmethod_form = self.pmethod_form(instance=request.user.userinfo.payment_method)
        return render(request, self.template_name, {
            'user_form': user_form,
            'userinfo_form': userinfo_form,
            'pmethod_form': pmethod_form,
        })

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        user_form = self.user_form(request.POST, instance=request.user)
        userinfo_form = self.userinfo_form(request.POST, instance=request.user.userinfo)
        pmethod_form = self.pmethod_form(request.POST, instance=request.user.userinfo.payment_method)
        if user_form.is_valid() and userinfo_form.is_valid() and pmethod_form.is_valid():
            user_form.save()
            userinfo_form.save()
            pmethod_form.save()
            messages.success(request, _('Your account was successfully updated!'))
            return redirect('user')
        else:
            messages.error(request, _('Please correct the error below.'))
        return render(request, self.template_name, {
            'user_form': user_form,
            'userinfo_form': userinfo_form,
            'pmethod_form': pmethod_form
        })


# User Registration Views	+
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            # add userinfo data
            user.userinfo.user_type = register_form.cleaned_data.get('user_type')
            user.save()
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        register_form = RegisterForm()
    return render(request, 'register.html', {'register_form': register_form})


def addCreditCardForm(request):
    pform_method = PaymentMethodForm
    template_name = 'creditcard_form.html'

    if request.POST:
        pmethod_form = pform_method(request.POST, instance=request.user.userinfo.payment_method)
        form = CreditCardFormSet(request.POST, instance=request.user.userinfo.payment_method)
        if form.is_valid() and pmethod_form.is_valid():
            pmethod_form.save()
            form.save()
            return redirect('home')
    else:
        pmethod_form = pform_method(instance=request.user.userinfo.payment_method)
        form = CreditCardFormSet(instance=request.user.userinfo.payment_method)

    return render(request, template_name, {
        "pmethod_form": pmethod_form,
        "form": form,
    })


def addBankAccountForm(request):
    pform_method = PaymentMethodForm
    template_name = 'bankaccount_form.html'

    if request.POST:
        pmethod_form = pform_method(request.POST, instance=request.user.userinfo.payment_method)
        form = BankAccountFormSet(request.POST, instance=request.user.userinfo.payment_method)
        if form.is_valid() and pmethod_form.is_valid():
            pmethod_form.save()
            form.save()
            return redirect('home')
    else:
        pmethod_form = pform_method(instance=request.user.userinfo.payment_method)
        form = BankAccountFormSet(instance=request.user.userinfo.payment_method)

    return render(request, template_name, {
        "pmethod_form": pmethod_form,
        "form": form,
    })
