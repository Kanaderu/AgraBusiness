from market.views import *
from django.urls import path

urlpatterns = [
    path('user/', EditUserView.as_view(), name='user'),
    path('user/add/cc/', AddCreditCardView.as_view(), name='cc'),
    path('user/add/bankaccount/', AddBankAccountView.as_view(), name='bankaccount'),
    path('register/', RegisterView.as_view(), name='register'),
    path('items/sell', SellProduceItemView.as_view(), name='produce-sell'),
    path('items/list', ProduceItemListView.as_view(), name='produce-list'),
    path('items/<int:pk>/', ProduceItemView.as_view(), name='produce-item'),
    path('items/<int:pk>/approve', ProduceItemApprove.as_view(), name='produce-approve'),
    path('items/<int:pk>/decline', ProduceItemDecline.as_view(), name='produce-decline'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/delete/<int:pk>/', DeleteCartItemView.as_view(), name='cartitem-delete'),
    path('cart/update/<int:pk>/', UpdateCartQtyView.as_view(), name='cartitem-update-qty'),
    path('checkout/payment', CheckoutPaymentView.as_view(), name='checkout-pay'),
    path('checkout/<int:pk>/shipment', CheckoutShipmentView.as_view(), name='checkout-ship'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
