from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    #url(r'^user/$', views.update_profile, {'template_name': 'user.html'}, name='user'),
    url(r'^user/$', views.update_profile, name='user'),
    #path('admin/', admin.site.urls),
]