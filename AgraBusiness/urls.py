"""AgraBusiness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.shortcuts import redirect


# redirect logged in user when accessing login page
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return auth_views.login(request, template_name='login.html')

urlpatterns = [
    re_path(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.password_reset_confirm, name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    re_path(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'), permanent=False), name="favicon"),
    path('market/', include('market.urls')),
    path('', TemplateView.as_view(template_name='home_landing.html'), name='landing'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    #path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    re_path(r'^login/', custom_login, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    path('admin/', admin.site.urls),
]
