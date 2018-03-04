from django.shortcuts import get_object_or_404, render
from .forms import DjangoUserForm, UserInfoForm, RegisterForm, PaymentMethodForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.translation import gettext as _


# Edit User Views
@login_required
@transaction.atomic
def edit_user(request):
    if request.method == 'POST':
        user_form = DjangoUserForm(request.POST, instance=request.user)
        userinfo_form = UserInfoForm(request.POST, instance=request.user.userinfo)
        pmethod_form = PaymentMethodForm(request.POST, instance=request.user.userinfo.payment_method)
        if user_form.is_valid() and userinfo_form.is_valid() and pmethod_form.is_valid():
            user_form.save()
            userinfo_form.save()
            pmethod_form.save()
            messages.success(request, _('Your account was successfully updated!'))
            return redirect('user')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = DjangoUserForm(instance=request.user)
        userinfo_form = UserInfoForm(instance=request.user.userinfo)
        pmethod_form = PaymentMethodForm(instance=request.user.userinfo.payment_method)
    return render(request, 'user.html', {
        'user_form': user_form,
        'userinfo_form': userinfo_form,
        'pmethod_form': pmethod_form
    })


# User Registration Views
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

