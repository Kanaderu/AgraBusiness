from . import views
from django.urls import path

urlpatterns = [
    path('user/', views.EditUserView.as_view(), name='user'),
    path('user/add/cc/', views.AddCreditCardView.as_view(), name='cc'),
    path('user/add/bankaccount/', views.AddBankAccountView.as_view(), name='bankaccount'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('items/list', views.ProduceItemListView.as_view(), name='produce-list'),
    path('items/<int:pk>/', views.ProduceItemView.as_view(), name='produce-item'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/delete/<int:pk>/', views.DeleteCartItemView.as_view(), name='cartitem-delete'),
]
