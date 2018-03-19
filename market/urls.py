from . import views
from django.urls import path

urlpatterns = [
    path('user/', views.EditUserView.as_view(), name='user'),
    path('user/add/cc/', views.addCreditCardForm, name='cc'),
    path('user/add/bankaccount/', views.addBankAccountForm, name='bankaccount'),
    path('register/', views.register, name='register'),
]
