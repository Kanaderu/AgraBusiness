from . import views
from django.urls import path

urlpatterns = [
    path('user/', views.edit_user, name='user'),
    path('register/', views.register, name='register'),
]
