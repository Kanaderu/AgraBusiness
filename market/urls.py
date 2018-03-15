from . import views
from django.urls import path

urlpatterns = [
    path('user/', views.EditUserView.as_view(), name='user'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
