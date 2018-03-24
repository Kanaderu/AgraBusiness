from django.shortcuts import get_object_or_404, render
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.utils import timezone


# Edit User View
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


# User Registration View
class RegisterView(View):
    register_form = RegisterForm
    template_name = 'register.html'

    decorators = [transaction.atomic]

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        register_form = self.register_form()

        return render(request, self.template_name, {'register_form': register_form})

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        register_form = self.register_form(self.request.POST)
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

        return render(request, self.template_name, {'register_form': register_form})


# User Add Credit Card View
class AddCreditCardView(View):
    pmethod_form = PaymentMethodForm
    creditcard_formset = CreditCardFormSet
    template_name = 'creditcard_form.html'

    decorators = [transaction.atomic, login_required]

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        pmethod_form = self.pmethod_form(instance=request.user.userinfo.payment_method)
        creditcard_formset = self.creditcard_formset(instance=request.user.userinfo.payment_method)

        return render(request, self.template_name, {
            "pmethod_form": pmethod_form,
            "creditcard_formset": creditcard_formset,
        })

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        pmethod_form = self.pmethod_form(request.POST, instance=request.user.userinfo.payment_method)
        creditcard_formset = self.creditcard_formset(request.POST, instance=request.user.userinfo.payment_method)

        if creditcard_formset.is_valid() and pmethod_form.is_valid():
            pmethod_form.save()
            creditcard_formset.save()
            return redirect('user')

        return render(request, self.template_name, {
            "pmethod_form": pmethod_form,
            "creditcard_formset": creditcard_formset,
        })


# User Add Bank Account View
class AddBankAccountView(View):
    pmethod_form = PaymentMethodForm
    bankaccount_formset = BankAccountFormSet
    template_name = 'bankaccount_form.html'

    decorators = [transaction.atomic, login_required]

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        pmethod_form = self.pmethod_form(instance=request.user.userinfo.payment_method)
        bankaccount_formset = self.bankaccount_formset(instance=request.user.userinfo.payment_method)

        return render(request, self.template_name, {
            "pmethod_form": pmethod_form,
            "bankaccount_formset": bankaccount_formset,
        })

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        pmethod_form = self.pmethod_form(request.POST, instance=request.user.userinfo.payment_method)
        bankaccount_formset = self.bankaccount_formset(request.POST, instance=request.user.userinfo.payment_method)

        if bankaccount_formset.is_valid() and pmethod_form.is_valid():
            pmethod_form.save()
            bankaccount_formset.save()
            return redirect('user')

        return render(request, self.template_name, {
            "pmethod_form": pmethod_form,
            "bankaccount_formset": bankaccount_formset,
        })


# Produce Item View
class ProduceItemView(ListView):
    model = ProduceItem
    template_name = 'produce_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context