from django.shortcuts import get_object_or_404, render
from .forms import DjangoUserForm, UserInfoForm, RegisterForm
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
        profile_form = UserInfoForm(request.POST, instance=request.user.userinfo)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('home')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = DjangoUserForm(instance=request.user)
        profile_form = UserInfoForm(instance=request.user.userinfo)
    return render(request, 'user.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# User Registration Views
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.userinfo.user_type = form.cleaned_data.get('user_type')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})