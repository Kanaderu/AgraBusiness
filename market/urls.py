from market.views import *
from django.urls import path

urlpatterns = [
    path('user/', EditUserView.as_view(), name='user'),
    path('user/add/cc/', AddCreditCardView.as_view(), name='cc'),
    path('user/add/bankaccount/', AddBankAccountView.as_view(), name='bankaccount'),
    path('register/', RegisterView.as_view(), name='register'),
    path('items/list', ProduceItemListView.as_view(), name='produce-list'),
    path('items/<int:pk>/', ProduceItemView.as_view(), name='produce-item'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/delete/<int:pk>/', DeleteCartItemView.as_view(), name='cartitem-delete'),
    path('cart/update/<int:pk>/', UpdateCartQtyView.as_view(), name='cartitem-update-qty'),
    path('checkout/payment', CheckoutPaymentView.as_view(), name='checkout-pay'),
    path('checkout/<int:pk>/shipment', CheckoutShipmentView.as_view(), name='checkout-ship'),
]
