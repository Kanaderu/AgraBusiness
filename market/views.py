from django.shortcuts import get_object_or_404, render
from .forms import DjangoUserForm, UserInfoForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.translation import gettext as _


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = DjangoUserForm(request.POST, instance=request.user)
        #profile_form = ProfileForm(request.POST, instance=request.user.profile)
        profile_form = UserInfoForm(request.POST, instance=request.user.userinfo)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('home')
            #return redirect('settings:user')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = DjangoUserForm(instance=request.user)
        #profile_form = ProfileForm(instance=request.user.profile)
        profile_form = UserInfoForm(instance=request.user.userinfo)
    return render(request, 'user.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
